from django.db import models
from core.utils import dnb
from django_ckeditor_5.fields import CKEditor5Field

from journals.models import Journal


class JournalNews(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name="news", **dnb)
    heading = models.TextField(**dnb)
    content = CKEditor5Field(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class JournalAnnouncement(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name="announcements", **dnb)
    heading = models.TextField(**dnb)
    content = CKEditor5Field(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"
