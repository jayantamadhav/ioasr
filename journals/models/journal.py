import re

from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote_plus
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import dnb


class Subject(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, **dnb)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            super(Subject, self).save(*args, **kwargs)
        self.url = re.sub(r"(\W+)", "-", self.name, 0, re.IGNORECASE).lower()
        super(Subject, self).save(*args, **kwargs)


class Journal(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="journals", **dnb
    )
    name = models.CharField(_("Journal Name"), max_length=256)
    abbreviation = models.CharField(_("Abbreviation Name"), max_length=256)
    url = models.CharField(_("URL"), max_length=256)
    issn_print = models.CharField(_("ISSN Print"), max_length=256, **dnb)
    issn_online = models.CharField(_("ISSN Online"), max_length=256, **dnb)
    email = models.CharField(_("Email"), max_length=256, null=True, blank=True)
    thumbnail = models.ImageField(
        _("Thumbnail"), upload_to="journals"
    )
    about = CKEditor5Field(**dnb)
    aim_and_scope = CKEditor5Field(**dnb)
    apc = models.CharField(_("Processing Charges"), max_length=256, **dnb)
    cite_score = models.FloatField(default=0.0)
    impact_factor = models.FloatField(default=0.0)
    acceptance_rate = models.CharField(_("Acceptance Rate"), max_length=50)
    first_decision = models.CharField(
        _("Time to First Decision (in days)"), max_length=50, **dnb
    )
    acceptance_to_publication = models.CharField(
        _("Acceptance to publication (in days)"), max_length=50, **dnb
    )
    review_time = models.CharField(_("Review Time"), max_length=50, **dnb)
    logo = models.ImageField(upload_to="journals", **dnb)

    primary_color = models.CharField(
        _("Primary HEX Color code"), max_length=20, default="#5C5470"
    )
    secondary_color = models.CharField(
        _("Secondary HEX Color code"), max_length=20, default="#352F44"
    )
    light_color = models.CharField(
        _("Light HEX Color code"), max_length=20, default="#FAF0E6"
    )
    submission_link = models.TextField(**dnb)

    def __str__(self) -> str:
        return f"{self.name}"


class Indexing(models.Model):
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="indexings"
    )
    name = models.TextField(**dnb)
    link = models.TextField(**dnb)
    image = models.ImageField(upload_to="indexings", **dnb)
    show_in_home = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"


EDITOR_TYPES = (
    ("editor_in_chief", "Editor-In-Chief"),
    ("managing_editor", "Managing Editor"),
    ("associate_editor", "Associate Editor"),
    ("editorial_board_member", "Editorial Board Member"),
    ("advisory_board_member", "Advisory Board Member"),
    ("reviewer", "Reviewer")
)


class EditorialBoard(models.Model):
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="editorial_board"
    )
    editor_type = models.CharField(
        max_length=32, choices=EDITOR_TYPES, default="editorial_board_member"
    )
    name = models.CharField(max_length=256)
    qualification = models.TextField(**dnb)
    designation = models.TextField(**dnb)
    institution = models.TextField(**dnb)
    image = models.ImageField(upload_to="editors", **dnb)

    def __str__(self):
        return self.name


class Policy(models.Model):
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="policies"
    )
    name = models.CharField(max_length=64, **dnb)
    url = models.CharField(max_length=64, **dnb)
    content = CKEditor5Field()

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            super(Policy, self).save(*args, **kwargs)
        self.url = re.sub(r"(\W+)", "-", self.name, 0, re.IGNORECASE).lower()
        super(Policy, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("policy", kwargs={"url": self.url})


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="categories"
    )
    category = models.CharField(_("Category"), max_length=255)
    created_at = models.DateField(auto_now_add=True)


class JournalAdConfig(models.Model):
    class Meta:
        verbose_name = "Ad Config"
        verbose_name_plural = "Ad Config"

    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="journal_ads"
    )
    ad_space_1 = models.ImageField(upload_to="ads", **dnb)
    ad_space_1_link = models.TextField(**dnb)
    ad_space_2 = models.ImageField(upload_to="ads", **dnb)
    ad_space_2_link = models.TextField(**dnb)
    responsive_ad_space_1 = models.ImageField(
        upload_to="ads", **dnb
    )
    responsive_ad_space_1_link = models.TextField(**dnb)
    responsive_ad_space_2 = models.ImageField(
        upload_to="ads", **dnb
    )
    responsive_ad_space_2_link = models.TextField(**dnb)

    def __str__(self):
        return f"{self.journal.name} Ad Config"
