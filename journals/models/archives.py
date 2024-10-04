# Create your models here.
import re
from django.db import models
from django.conf import settings
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.utils import dnb
from journals.citation_generator import GenerateCitation
from journals.models.journal import Journal



class Volume(models.Model):
    in_press = models.BooleanField(default=False)
    journal = models.ForeignKey(
        Journal, on_delete=models.CASCADE, related_name="volumes"
    )
    name = models.CharField(_("Volume Name"), max_length=32)
    year = models.CharField(_("Year"), max_length=32)

    def __str__(self) -> str:
        return f"{self.journal.name} | {self.name}"


class Issue(models.Model):
    in_press = models.BooleanField(default=False)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, related_name="issues")
    name = models.CharField(_("Issue Name"), max_length=32)
    month = models.CharField(_("Month"), max_length=32, **dnb)
    is_special_issue = models.BooleanField(
        verbose_name="This is a Special Issue", default=False
    )
    title = models.TextField(verbose_name="Special Issue Title", **dnb)
    about = CKEditor5Field(verbose_name="Special Issue About", **dnb)
    thumbnail = models.ImageField(upload_to="issues", verbose_name="Special Issue Cover", **dnb)
    submission_deadline = models.DateField(
        verbose_name="Special Issue Submission Deadline", **dnb
    )
    is_published = models.BooleanField(
        verbose_name="This Speical Issue is published?", default=False
    )
    published = models.DateField(verbose_name="Special Issue Published Date", **dnb)

    def __str__(self) -> str:
        return f"{self.volume.journal.name } | {self.volume.name}  {self.name}"

    def get_absolute_url(self):
        return reverse(
            "archive-details", kwargs={"vol": self.volume.pk, "issue": self.pk}
        )


class SpecialIssueGuestEditor(models.Model):
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="guest_editors"
    )
    name = models.CharField(_("Full Name"), max_length=256)
    email = models.CharField(max_length=256, **dnb)
    orcid_id = models.CharField(max_length=256, **dnb)
    affiliation = models.TextField(_("Affilication"), **dnb)
    qualification = models.TextField(_("Qualification"), **dnb)

    def __str__(self) -> str:
        return f"{self.name}"


ARTICLE_TYPES = (
    ("Research Article", "Research Article"),
    ("Mini Review Article", "Mini Review Article"),
    ("Commentary Article", "Commentary Article"),
    ("Review Article", "Review Article"),
    ("Short Communication", "Short Communication"),
    ("Short Commentary Article", "Short Commentary Article"),
    ("Case Report", "Case Report"),
    ("Case Series", "Case Series"),
    ("Clinical Images", "Clinical Images"),
    ("Editor's pick", "Editor's pick"),
    ("Editorial", "Editorial"),
    ("Elective Report", "Elective Report"),
    ("Letter to the Editor", "Letter to the Editor"),
    ("News Article", "News Article"),
    ("News Section", "News Section"),
    ("Original Article", "Original Article"),
    ("Perspective Article", "Perspective Article"),
)

ARTICLE_TYPE_ABBR = {
    "Research Article": "ra",
    "Mini Review Article": "mra",
    "Commentary Article": "ca",
    "Review Article": "ra",
    "Short Communication": "sc",
    "Short Commentary Article": "sca",
    "Case Report": "cr",
    "Case Series": "cs",
    "Clinical Images": "ci",
    "Editor's pick": "ep",
    "Editorial": "ed",
    "Elective Report": "er",
    "Letter to the Editor": "le",
    "News Article": "na",
    "News Section": "ns",
    "Original Article": "oa",
    "Perspective Article": "pa",
}


class Article(models.Model):
    in_press = models.BooleanField(default=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="articles")
    url = models.TextField(**dnb)
    article_type = models.CharField(
        _("Article Type"), max_length=128, choices=ARTICLE_TYPES
    )
    title = models.TextField()
    doi = models.CharField(_("DOI"), max_length=256, **dnb)
    doi_link = models.TextField(_("DOI Link"), **dnb)
    pmid = models.CharField(_("PMID"), max_length=256, **dnb)
    pmid_link = models.TextField(_("PMID Link"), **dnb)
    abstract = CKEditor5Field(**dnb)
    page_from = models.PositiveIntegerField(**dnb)
    page_to = models.PositiveIntegerField(**dnb)
    keywords = models.TextField(**dnb)
    how_to_cite = CKEditor5Field(**dnb)
    pdf = models.FileField(upload_to="articles", **dnb)
    xml = models.FileField(upload_to="articles", **dnb)
    received = models.DateField(**dnb)
    revised = models.DateField(**dnb)
    accepted = models.DateField(**dnb)
    published = models.DateField(**dnb)
    available_on = models.DateField(**dnb)
    is_open_access = models.BooleanField(default=True)
    downloads = models.PositiveBigIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    
    apa = models.TextField(**dnb)
    mla = models.TextField(**dnb)
    chicago = models.TextField(**dnb)
    vancouver = models.TextField(**dnb)
    harvard = models.TextField(**dnb)

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("journals:article", kwargs={"url": self.issue.volume.journal.url, "vol": self.issue.volume.pk, "issue": self.issue.pk, "article_url": self.url})

@receiver(post_save, sender=Article)
def article_post_save(sender, instance: Article, created, **kwargs):
    post_save.disconnect(article_post_save, sender=sender)
    if not instance.url:
        instance.url = re.sub(r"(\W+)", "-", instance.title, 0, re.IGNORECASE).lower()
        instance.url += f"-{instance.pk}"
    
    journal = Journal.objects.get(name=instance.issue.volume.journal.name)
    authors = ArticleAuthor.objects.filter(article=instance)
    citations = GenerateCitation(
        journal, instance.issue.volume, instance.issue, instance, authors
    )
    citations.generate()
    instance.apa = citations.APA
    instance.mla = citations.MLA
    instance.chicago = citations.Chicago
    instance.harvard = citations.Harvard
    instance.vancouver = citations.Vancouver

    instance.save()
    post_save.connect(article_post_save, sender=Article)


class ArticleAuthor(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="authors"
    )
    prefix = models.CharField(_("Prefix"), max_length=256, **dnb)
    first_name = models.CharField(_("First Name"), max_length=256)
    middle_name = models.CharField(_("Middle Name"), max_length=256, **dnb)
    last_name = models.CharField(_("Last Name"), max_length=256, **dnb)
    email = models.CharField(max_length=256, **dnb)
    orcid_id = models.CharField(max_length=256, **dnb)
    affiliation = models.TextField(_("Affilication"), **dnb)
    qualification = models.TextField(_("Qualification"), **dnb)


    def __str__(self) -> str:
        return f"{self.first_name}{' ' if self.middle_name else ''}{self.middle_name or ''}{' ' if self.last_name else ''}{self.last_name or ''}"
    
    @property
    def full_name(self) -> str:
        return f"{self.prefix + ' ' if self.prefix else ''}{self.first_name}{' ' if self.middle_name else ''}{self.middle_name or ''}{' ' if self.last_name else ''}{self.last_name or ''}"


class ArticleSection(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="sections"
    )
    heading = models.CharField(max_length=256, **dnb)
    content = CKEditor5Field(**dnb)

    def __str__(self) -> str:
        return f"{self.heading}"
