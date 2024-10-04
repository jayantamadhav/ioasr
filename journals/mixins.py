from core.mixins import PublisherMixin
from journals.models import Journal
from journals.models.journal import JournalAdConfig, Policy

class JournalMixin(PublisherMixin):
    def get_context_data(self, **kwargs):
        # Access kwargs here or perform any actions with them
        try:
            journal = Journal.objects.get(url=kwargs.get("url"))
            policies = Policy.objects.filter(journal=journal)
        except Journal.DoesNotExist:
            policies = None
            journal = None

        print(policies)

        try:
            ads = JournalAdConfig.objects.filter(journal=journal).first()
        except:
            ads = None

        context = super().get_context_data(**kwargs)

        # Add or modify context data if needed
        context.update({
            "journal": journal, 
            "ads": ads,
            "policies": policies
        })

        return context