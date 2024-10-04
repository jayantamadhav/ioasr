from core.models import Information, Membership, SiteConfiguration
from journals.models.journal import Journal

class PublisherMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        

        context.update({
            "informations": Information.objects.all(),
            "journal_list": Journal.objects.order_by("name").values_list('name', flat=True),
            "site_config": SiteConfiguration.get_solo(),
            "memberships": Membership.objects.all().order_by("-pk")
        })

        return context