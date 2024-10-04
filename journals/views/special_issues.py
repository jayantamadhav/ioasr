
from django.shortcuts import render
from django.views.generic import TemplateView

from journals.mixins import JournalMixin
from journals.models import Issue, Volume, Article


class JournalSpecialIssueAbout(JournalMixin, TemplateView):
    template_name = "journals/archives/special-issue/about.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        return render(request, self.template_name, ctx)
    
class JournalSpecialIssuePropose(JournalMixin, TemplateView):
    template_name = "journals/archives/special-issue/propose.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        return render(request, self.template_name, ctx)
    
class JournalSpecialIssueOpen(JournalMixin, TemplateView):
    template_name = "journals/archives/special-issue/open.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        open_si = Issue.objects.filter(volume__journal=ctx.get("journal"), is_special_issue=True, is_published=False).order_by("-submission_deadline")
        ctx.update({
            "special_issues": open_si
        })
        return render(request, self.template_name, ctx)
    
class JournalSpecialIssuePublished(JournalMixin, TemplateView):
    template_name = "journals/archives/special-issue/published.html"
    
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        published_si = Issue.objects.filter(volume__journal=ctx.get("journal"), is_special_issue=True, is_published=True).order_by("-published")
        ctx.update({
            "special_issues": published_si
        })
        return render(request, self.template_name, ctx)
    
class JournalSpecialIssueDetails(JournalMixin, TemplateView):
        template_name = "journals/archives/special-issue/details.html"
    
        def get(self, request, *args, **kwargs):
            ctx = self.get_context_data(**kwargs)
            issue = Issue.objects.get(id=kwargs.get("issue"))
            ctx.update({
                "articles": Article.objects.filter(issue=issue).order_by("-published"),
                "volume": issue.volume,
                "issue": issue
            })
            return render(request, self.template_name, ctx)
        