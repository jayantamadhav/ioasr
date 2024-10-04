from django.db.models import Q, Func, Value, CharField, functions
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render

from journals.mixins import JournalMixin
from journals.models import Article, ArticleAuthor, Policy


class JournalAuthorPublicationsView(JournalMixin, TemplateView):
    template_name = "journals/search/author-publications.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        if request.GET.get("author"):
            author = ArticleAuthor.objects.filter(
                id=request.GET.get("author")
            ).first()
            fullname = f"{author.first_name} {author.middle_name if author.middle_name else ''} {author.last_name}"
            articles = Article.objects.annotate(
                fullname=Func(
                    functions.Coalesce('authors__first_name', Value("")),
                    Value(" "),
                    functions.Coalesce('authors__middle_name', Value("")),
                    Value(" "),
                    functions.Coalesce('authors__last_name', Value("")),
                    function='CONCAT',
                    output_field=CharField()
                )
            ).filter(fullname__icontains=fullname, issue__volume__journal=ctx.get("journal"))
            ctx.update(
                {"author": author, "articles": articles, "count": articles.count()}
            )
        else:
            return redirect("core:error")
        return render(request, self.template_name, ctx)
    
class JournalPolicyView(JournalMixin, TemplateView):
    template_name = "journals/policy.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        policy_url = kwargs.get("policy_url")
        try:
            ctx["policy"] = (
                Policy.objects.filter(url=policy_url).order_by("-id").first()
            )
        except Policy.DoesNotExist:
            ctx["policy"] = None
        return render(request, self.template_name, ctx)