from typing import Any
from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.mixins import PublisherMixin
from core.models import Membership, Member


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
