import os
import re
import requests
import mimetypes
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseNotAllowed,
    StreamingHttpResponse,
)
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from journals.models import Volume, Issue, Article, ArticleAuthor
from journals.mixins import JournalMixin


class JournalArchiveListView(JournalMixin, TemplateView):
    template_name = "journals/archives/list.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx.update(
            {
                "volumes": Volume.objects.filter(journal=ctx.get("journal")).order_by(
                    "-year"
                )
            }
        )
        return self.render_to_response(ctx)


class JournalArchiveDetailsView(JournalMixin, TemplateView):
    template_name = "journals/archives/details.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        try:
            issue = Issue.objects.get(id=kwargs.get("issue"))
            ctx.update(
                {
                    "articles": Article.objects.filter(issue=issue).order_by(
                        "-published"
                    ),
                    "volume": issue.volume,
                    "issue": issue,
                }
            )
        except:
            return redirect("error")
        return self.render_to_response(ctx)


class JournalArticleView(JournalMixin, TemplateView):
    template_name = "journals/archives/article.html"

    def split_keywords(self, article: Article):
        if article.keywords:
            split_list = re.split(r"(?<!^);|(?!^),", article.keywords)
            return [word.lstrip().rstrip() for word in split_list if word.strip()]
        else:
            return []

    def get(self, request, *args, **kwargs):
        try:
            ctx = self.get_context_data(**kwargs)
            article = Article.objects.get(url=kwargs.get("article_url"))
            article.views += 1
            article.save()
            journal = article.issue.volume.journal
            ctx["recommended"] = Article.objects.filter(
                issue__volume__journal=journal, keywords__icontains=article.keywords
            ).exclude(id=article.id)[:5]

            if not ctx["recommended"]:
                ctx["recommended"] = (
                    Article.objects.filter(issue__volume__journal=journal)
                    .order_by("views")
                    .exclude(id=article.id)[:4]
                )

            affiliations = {}
            aff_counter = 1
            for author in ArticleAuthor.objects.filter(article=article):
                if author.affiliation not in affiliations:
                    affiliations.update({author.affiliation: aff_counter})
                    aff_counter += 1
            authors = []
            for author in ArticleAuthor.objects.filter(article=article):
                temp = author.__dict__
                temp.update(
                    {
                        "full_name": author.full_name,
                        "author_affiliation_id": (
                            affiliations.get(author.affiliation)
                            if author.affiliation
                            else None
                        ),
                    }
                )
                authors.append(temp)
            ctx.update(
                {
                    "authors": authors,
                    "affiliations": affiliations,
                    "article": article,
                    "keywords": self.split_keywords(article),
                }
            )
        except Exception as e:
            print(e)
            return redirect("core:error")
        return self.render_to_response(ctx)


class ArticleXMLDownloadView(View):
    def get(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=kwargs.get("article_id"))
            article.downloads += 1
            article.save()

            file_url = article.xml.url

            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Ensure the request was successful

            filename = os.path.basename(file_url)
            mime_type, _ = mimetypes.guess_type(filename)

            streaming_response = StreamingHttpResponse(
                response.iter_content(chunk_size=8192),
                content_type=mime_type or "application/pdf",
            )
            streaming_response["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )
            return streaming_response
        except:
            return redirect("error")


class ArticleDownloadView(View):

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get("article_id")))
        article.downloads += 1
        article.save()

        self.send_subscriber(request.POST.get("email"))

        try:
            file_url = article.pdf.url

            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Ensure the request was successful

            filename = os.path.basename(file_url)
            mime_type, _ = mimetypes.guess_type(filename)

            streaming_response = StreamingHttpResponse(
                response.iter_content(chunk_size=8192),
                content_type=mime_type or "application/pdf",
            )
            streaming_response["Content-Disposition"] = (
                f'attachment; filename="{filename}"'
            )
            return streaming_response
        except:
            return redirect(
                reverse(
                    "journals:article",
                    kwargs={
                        "url": article.issue.volume.journal.url,
                        "vol": article.issue.volume.pk,
                        "issue": article.issue.pk,
                        "article_url": article.url,
                    },
                )
            )

    def send_subscriber(self, email):
        IARCON_API_BASE = os.getenv("IARCON_API_BASE")
        url = f"{IARCON_API_BASE}/webapp/subscriber"
        data = {"email": email, "from": "iarconsortium.org"}
        AUTH_TOKEN = os.getenv("IARCON_TOKEN")
        headers = {"Authorization": AUTH_TOKEN, "Content-Type": "application/json"}
        requests.post(url, json=data, headers=headers)
        
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
