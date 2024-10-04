from django.views.generic import TemplateView
from itertools import chain
from django.db.models import Q, Func, Value, CharField, functions
from django.shortcuts import redirect

from core.mixins import PublisherMixin
from journals.models import (
    Indexing,
    EditorialBoard,
    Article,
    JournalNews,
    JournalAnnouncement,
)
from journals.mixins import JournalMixin


class JournalDetailView(JournalMixin, TemplateView):
    template_name = "journals/home.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        articles = Article.objects.filter(issue__volume__journal=ctx.get("journal"))
        ctx.update(
            {
                "editor": EditorialBoard.objects.filter(
                    journal=ctx.get("journal"), editor_type="editor_in_chief"
                ).first(),
                "latest_published": articles.order_by("-published")[:8],
                "most_downloaded": articles.order_by("-downloads")[:8],
                "most_popular": articles.order_by("-views")[:8],
                "news": JournalNews.objects.filter(journal=ctx.get("journal")).order_by(
                    "-created_on"
                )[:2],
                "announcements": JournalAnnouncement.objects.filter(
                    journal=ctx.get("journal")
                ).order_by("-created_on")[:2],
                "indexings": Indexing.objects.filter(
                    journal=ctx.get("journal"), show_in_home=True
                ).order_by("name"),
                "editor_in_chiefs": EditorialBoard.objects.filter(
                    journal=ctx.get("journal"), editor_type="editor_in_chief"
                ),
            }
        )
        return self.render_to_response(ctx)


class JournalInsightsView(JournalMixin, TemplateView):
    template_name = "journals/insights.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        print(ctx)
        indexings = Indexing.objects.filter(journal=ctx.get("journal")).order_by("name")
        ctx.update({"indexings": indexings})
        return self.render_to_response(ctx)


class JournalAboutView(JournalMixin, TemplateView):
    template_name = "journals/about/about.html"
    about_type_map = {
        "aim-and-scope": "Aim & Scope",
        "editorial-board": "Editorial Board",
        "news": "News",
        "announcements": "Announcements",
    }

    def get(self, request, *args, **kwargs):
        about_type = kwargs.get("about_type")
        if about_type not in self.about_type_map.keys():
            return redirect("core:error")
        ctx = self.get_context_data(**kwargs)
        ctx.update(
            {
                "about_type": about_type,
                "about_type_label": self.about_type_map[about_type],
            }
        )

        if about_type == "editorial-board":
            editorial_board = EditorialBoard.objects.filter(journal=ctx.get("journal"))
            ctx.update(
                {
                    "editor_in_chief": editorial_board.filter(
                        editor_type="editor_in_chief"
                    ),
                    "associate_editor": editorial_board.filter(
                        editor_type="associate_editor"
                    ),
                    "editorial_board_member": editorial_board.filter(
                        editor_type="editorial_board_member"
                    ),
                    "advisory_board_member": editorial_board.filter(
                        editor_type="advisory_board_member"
                    ),
                    "managing_editor": editorial_board.filter(
                        editor_type="managing_editor"
                    ),
                    "reviewers": editorial_board.filter(
                        editor_type="reviewer"
                    ),
                }
            )
        elif about_type == "news":
            ctx.update({"news": None})
        elif about_type == "announcements":
            ctx.update({"announcements": None})
        return self.render_to_response(ctx)


class SearchView(JournalMixin, TemplateView):
    template_name = "journals/search/results.html"

    def get(self, request, *args, **kwargs):
        if not request.GET.get("q"):
            return redirect("core:error")
        # try:
        results = None
        ctx = self.get_context_data(**kwargs)
        query = request.GET.get("q")
        all_articles = Article.objects.filter(
            issue__volume__journal=ctx["journal"]
        ).filter(
            Q(title__icontains=query)
            | Q(abstract__icontains=query)
            | Q(keywords__icontains=query)
        )
        author_articles = Article.objects.filter(authors__first_name__icontains=query)
        count = all_articles.count() + author_articles.count()
        articles = list(chain(all_articles, author_articles))
        ctx.update({"query": query, "articles": articles, "count": count})
        return self.render_to_response(ctx)
        # except:
        #     return redirect("core:error")
