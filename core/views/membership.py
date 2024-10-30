from typing import Any
from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from core.mixins import PublisherMixin
from core.models import Membership, Member, MembershipApplication


class MembershipInfoView(PublisherMixin, TemplateView):
    template_name = "core/memberships/membership-info.html"

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        try:
            membership = Membership.objects.get(url=kwargs.get("url"))
            members = Member.objects.filter(membership=membership).order_by("-pk")
            ctx.update({
                "membership": membership,
                "members": members
            })
            return render(request, self.template_name, ctx)
        except:
            return redirect("core:error")


class MembershipApplicationView(PublisherMixin, TemplateView):
    template_name = "core/memberships/application.html"
    
    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(*args, **kwargs)
        try:
            application = MembershipApplication.objects.create(
                membership_type=request.POST.get("membership_type"),
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                qualification=request.POST.get("qualification"),
                affiliation=request.POST.get("affiliation"),
                specialization=request.POST.get("specialization"),
                image=request.FILES.get("image")
            )
            application.save()
            messages.success(request, "Application submitted successfully")
        except:
            messages.error(request, "There was an error while processing your application")
        return self.render_to_response(ctx)