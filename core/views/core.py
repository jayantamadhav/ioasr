import json
from typing import Any
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.serializers import serialize
from django.db.models import Q
from django.views.generic import TemplateView, View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse

from core.mixins import PublisherMixin
from core.models import News, Announcement
from core.models.core import Application, Blog, HardCopyOrder, Information, NewsletterSubscription
from journals.models import Journal, Subject, Article
from journals.models.archives import Issue, Volume


class HomeView(PublisherMixin, TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        journals = Journal.objects.all().order_by("name")
        ctx.update(
            {
                "journals": journals[:6],
                "subjects": Subject.objects.all().order_by("name"),
                "articles": Article.objects.all().order_by("-published")[:7],
                "news": News.objects.all().order_by("-created_on")[:3],
                "blogs": Blog.objects.all().order_by("-created_at")[:4],
                "announcements": Announcement.objects.all().order_by("-created_on")[:3],
            }
        )
        return render(request, self.template_name, ctx)

class ErrorView(PublisherMixin, TemplateView):
    template_name = "core/error.html"

class AboutUsView(PublisherMixin, TemplateView):
    template_name = "core/about.html"

class ContactUsView(PublisherMixin, TemplateView):
    template_name = "core/contact.html"

class PrivacyPolicyView(PublisherMixin, TemplateView):
    template_name = "core/policies/privacy-policy.html"


class RefundPolicyView(PublisherMixin, TemplateView):
    template_name = "core/policies/refund-policy.html"


class TermsAndConditionsView(PublisherMixin, TemplateView):
    template_name = "core/policies/terms-and-conditions.html"


class BrowseJournalView(PublisherMixin, TemplateView):
    template_name = "core/browse-journals.html"

    def get(self, request, *args: Any, **kwargs: Any):
        ctx = self.get_context_data(*args, **kwargs)
        subjects = Subject.objects.all().order_by("name")
        if not request.GET.get("subject"):
            subject_name = "All"
            journals = Journal.objects.all().order_by("name")
        else:
            subject = Subject.objects.get(url=request.GET.get("subject"))
            subject_name = subject.name
            journals = Journal.objects.filter(subject=subject).order_by("name")

        ctx.update(
            {"subjects": subjects, "subject_name": subject_name, "journals": journals}
        )
        return self.render_to_response(ctx)


class NewsListView(PublisherMixin, TemplateView):
    template_name = "core/news/list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        if request.GET.get("query"):
            news_list = News.objects.filter(
                Q(heading__icontains=request.GET.get("query"))
                | Q(content__icontains=request.GET.get("query"))
            )
        else:
            news_list = News.objects.all().order_by("-created_on")

        paginator = Paginator(news_list, self.paginate_by)
        page = request.GET.get("page")

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            news = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page.
            news = paginator.page(paginator.num_pages)

        ctx.update(
            {
                "latest_news": News.objects.all().order_by("-created_on")[:3],
                "latest_announcements": Announcement.objects.all().order_by(
                    "-created_on"
                )[:3],
                "news": news,
            }
        )
        return self.render_to_response(ctx)


class NewsDetailsView(PublisherMixin, TemplateView):
    template_name = "core/news/details.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            news = News.objects.get(pk=kwargs.get("pk"))
        except News.DoesNotExist:
            news = None
        context.update({"news": news})
        return context


class AnnouncementListView(PublisherMixin, TemplateView):
    template_name = "core/announcements/list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        if request.GET.get("query"):
            announcement_list = Announcement.objects.filter(
                Q(heading__icontains=request.GET.get("query"))
                | Q(content__icontains=request.GET.get("query"))
            )
        else:
            announcement_list = Announcement.objects.all().order_by("-created_on")

        paginator = Paginator(announcement_list, self.paginate_by)
        page = request.GET.get("page")

        try:
            announcements = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            announcements = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page.
            announcements = paginator.page(paginator.num_pages)

        ctx.update(
            {
                "latest_news": News.objects.all().order_by("-created_on")[:3],
                "latest_announcements": Announcement.objects.all().order_by(
                    "-created_on"
                )[:3],
                "announcements": announcements,
            }
        )
        return self.render_to_response(ctx)


class AnnouncementDetailsView(PublisherMixin, TemplateView):
    template_name = "core/announcements/details.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            announcement = Announcement.objects.get(pk=kwargs.get("pk"))
        except News.DoesNotExist:
            announcement = None
        context.update({"announcement": announcement})
        return context


class InformationDetailsView(PublisherMixin, TemplateView):
    template_name = "core/information/information.html"

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        try:
            informations = Information.objects.all()
            information = informations.get(url=kwargs.get("url"))
        except:
            return redirect("core:error")
        ctx.update({"information": information, "informations": informations})
        return self.render_to_response(ctx)


class SubscribeNewsletterView(PublisherMixin, View):
    def post(self, request, *args, **kwargs):
        referring_url = request.META.get("HTTP_REFERER", None)

        sn = NewsletterSubscription.objects.get_or_create(
            email=request.POST.get("email")
        )

        if referring_url:
            return redirect(referring_url)
        return redirect("core:home")


class SearchView(PublisherMixin, ListView):
    model = Article
    template_name = "core/search.html"
    # context_object_name = "articles"
    # paginate_by = 50

    articleTypes = [
        "All",
        "Research Article",
        "Mini Review Article",
        "Commentary Article",
        "Review Article",
        "Short Communication",
        "Short Commentary Article",
        "Case Report",
        "Case Series",
        "Clinical Images",
        "Editor's pick",
        "Editorial",
        "Elective Report",
        "Letter to the Editor",
        "News Article",
        "News Section",
        "Original Article",
        "Perspective Article",
    ]

    def get_queryset(self):
        article_type = self.request.GET.get("articleType")
        keywords = self.request.GET.get("keywords")
        author = self.request.GET.get("author")
        journal = self.request.GET.get("journal")

        try:
            if article_type and article_type not in self.articleTypes:
                raise Exception("Invalid article type")

            articles = Article.objects.all()
            
            if keywords:
                query = Q()
                if len(keywords.split()) < 3:
                    for word in keywords.split():
                        query |= Q(keywords__icontains=word) | Q(title__icontains=word)
                else:
                    query = Q(title__icontains=keywords) | Q(keywords__icontains=keywords)
                    
                articles = articles.filter(query)

            if author:
                query = Q()
                for word in author.split():
                    query |= Q(authors__first_name=word) | Q(authors__middle_name=word) | Q(authors__last_name=word)
                articles = articles.filter(query)

            if journal and journal != "All":
                journal_obj = Journal.objects.get(name=journal)
                articles = articles.filter(issue__volume__journal=journal_obj)

            if article_type and article_type != "All":
                articles = articles.filter(article_type=article_type)

            return articles

        except Exception as e:
            print(f"Error: {e}")
            return (
                Article.objects.none()
            )
        
    def get_context_data(self, **kwargs):
        # Add variables to the context dictionary
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        context["articleType"] = self.request.GET.get("articleType")
        context["keywords"] = self.request.GET.get("keywords")
        context["author"] = self.request.GET.get("author")
        context["journal"] = self.request.GET.get("journal")
        return context


class JoinAsEditorView(PublisherMixin, TemplateView):
    template_name = "core/join-as/editor.html"

    def post(self, request, *args, **kwargs):
        try:
            ctx = self.get_context_data(**kwargs)
            application = Application.objects.create(
                application_for = "Editor",
                email = request.POST.get("email"),
                name = request.POST.get("name"),
                phone = request.POST.get("phone"),
                spcialization = request.POST.get("spcialization"),
                affiliation = request.POST.get("affiliation"),
                publications = request.POST.get("publications"),
                photo = request.POST.get("photo"),
                result = request.POST.get("result"),
            )
            application.save()
            messages.success(request, "Your application has been submitted successfully")        
            return self.render_to_response(ctx)
        except Exception as e:
            print(str(e))
            return redirect("core:error")
    

class JoinAsReviewerView(PublisherMixin, TemplateView):
    template_name = "core/join-as/reviewer.html"

    def post(self, request, *args, **kwargs):
        try:
            ctx = self.get_context_data(**kwargs)
            application = Application.objects.create(
                application_for = "Reviewer",
                email = request.POST.get("email"),
                name = request.POST.get("name"),
                phone = request.POST.get("phone"),
                spcialization = request.POST.get("spcialization"),
                affiliation = request.POST.get("affiliation"),
                publications = request.POST.get("publications"),
                photo = request.POST.get("photo"),
                result = request.POST.get("result"),
            )
            application.save()
            messages.success(request, "Your application has been submitted successfully")        
            return self.render_to_response(ctx)
        except Exception as e:
            print(str(e))
            return redirect("core:error")
        
class HardCopyOrderView(PublisherMixin, TemplateView):
    template_name = "core/hard-copy-order.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx.update({
            "journals": Journal.objects.all().order_by("name")
        })

        try:
            if request.GET.get("journal"):
                journal = Journal.objects.get(pk=int(request.GET.get("journal")))
                volumes = Volume.objects.filter(journal=journal)
                volumes_data = serialize('json', volumes)
                return JsonResponse(volumes_data, safe=False)

            if request.GET.get("volume"):
                volume = Volume.objects.get(pk=int(request.GET.get("volume")))
                issues = Issue.objects.filter(volume=volume)
                issues_data = serialize('json', issues)
                return JsonResponse(issues_data, safe=False)
            
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {e}")
            return redirect("core:home")
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        try:
            ctx = self.get_context_data(**kwargs)
            ctx.update({
                "journals": Journal.objects.all().order_by("name")
            })
            if not request.POST.get("ohc-issues"):
                messages.warning(request, "Please select atleast one issue")
            else:
                issues = ""
                for issue_id in request.POST.getlist("ohc-issues"):
                    print(issue_id)
                    _issue = Issue.objects.get(pk=int(issue_id))
                    issues += f"{_issue.name}, "

                order = HardCopyOrder.objects.create(
                    email=request.POST.get("ohc-email"),
                    name=request.POST.get("ohc-name"),
                    phone=request.POST.get("ohc-phone"),
                    journal=request.POST.get("ohc-journal"),
                    volume=request.POST.get("ohc-volume"),
                    issues=issues,
                    copies=request.POST.get("ohc-copies"),
                    address1=request.POST.get("ohc-address1"),
                    address2=request.POST.get("ohc-address2"),
                    remarks=request.POST.get("ohc-remarks"),
                )
                order.save()

                messages.success(request, "We have received your request, our representative will contact you shortly")
            return self.render_to_response(ctx)
        except Exception as e:
            print(str(e))
            return redirect("core:error")

  
class SubmitResearchView(PublisherMixin, TemplateView):
    template_name = "core/submit-research.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx.update({
            "journals": Journal.objects.all().order_by("name")
        })
        return self.render_to_response(ctx)
    
