from typing import Any
from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.mixins import PublisherMixin
from core.models import Blog, BlogAuthor


class BlogListView(PublisherMixin, TemplateView):
    template_name = "core/blogs/list.html"

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all().order_by("-created_at")
        ctx = {"recent_blogs": blogs[:3], "blogs": blogs.order_by("-views")[3:]}
        return render(request, self.template_name, ctx)


class BlogDetailsView(PublisherMixin, TemplateView):
    template_name = "core/blogs/details.html"

    def get(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(url=kwargs.get("url"))
            recommended_blogs = Blog.objects.all().exclude(pk=blog.pk).order_by("-views")[:4]
            ctx = {"blog": blog, "recommended_blogs": recommended_blogs}

            return render(request, self.template_name, ctx)
        except:
            return redirect("core:error")
