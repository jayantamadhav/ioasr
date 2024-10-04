import re
from django.urls import reverse
from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _

from core.utils import dnb


class About(models.Model):
    show_in_footer = models.BooleanField(default=False)
    heading = models.CharField(max_length=255)
    content = CKEditor5Field(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"


class News(models.Model):
    heading = models.TextField(_("Heading"))
    content = CKEditor5Field(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Announcement(models.Model):
    heading = models.TextField(_("Heading"))
    content = CKEditor5Field(**dnb)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.heading}"


class Book(models.Model):
    title = models.TextField(_("Title"))
    isbn_online = models.CharField(max_length=256, **dnb)
    isbn_print = models.CharField(max_length=256, **dnb)
    doi = models.CharField(max_length=256, **dnb)
    doi_link = models.CharField(max_length=256, **dnb)
    about = models.TextField(**dnb)
    pdf = models.FileField(**dnb)
    flyer = models.FileField(**dnb)
    cover = models.ImageField(upload_to="book-covers",**dnb)
    price = models.CharField(max_length=256, **dnb)
    format = models.CharField(max_length=256, **dnb)
    published = models.DateField(**dnb)

    def __str__(self):
        return f"{self.title}"


class Information(models.Model):
    name = models.CharField(max_length=255, **dnb)
    content = CKEditor5Field()
    url = models.CharField(max_length=255, **dnb)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.url = re.sub(r"(\W+)", "-", self.name, 0, re.IGNORECASE).lower()
        super(Information, self).save(*args, **kwargs)


class FooterKeyword(models.Model):
    class Meta:
        verbose_name = "Footer Keywords"
        verbose_name_plural = "Footer Keywords"

    keyword = models.CharField(_("Keyword"), max_length=255, **dnb)
    link = models.TextField(**dnb)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.keyword}"


class NewsletterSubscription(models.Model):
    email = models.CharField(_("Email"), max_length=255, **dnb)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"


class Blog(models.Model):
    url = models.TextField(**dnb)
    heading = models.TextField()
    content = CKEditor5Field(**dnb)
    featured_image = models.ImageField(upload_to="blogs", **dnb)
    keywords = models.TextField(**dnb)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.heading}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Blog, self).save(*args, **kwargs)
        if not self.url:
            self.url = re.sub(r"(\W+)", "-", self.heading, 0, re.IGNORECASE).lower()
        return super(Blog, self).save(*args, **kwargs)


class BlogAuthor(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_authors"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, **dnb)
    profile_link = models.TextField(**dnb)
    about = models.TextField(**dnb)
    profile_photo = models.ImageField(upload_to="blog_authors", **dnb)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


APPLICATION_FOR_CHOICES = (
    ("Editor", "Editor"),
    ("Reviewer", "Reviewer"),
)


class Application(models.Model):
    application_for = models.CharField(
        max_length=255, choices=APPLICATION_FOR_CHOICES, default="Editor"
    )
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    spcialization = models.TextField(**dnb)
    affiliation = models.TextField(**dnb)
    publications = models.TextField(**dnb)
    photo = models.ImageField(upload_to="applications")
    result = models.FileField(upload_to="applications")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"


class HardCopyOrder(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    journal = models.CharField(max_length=255)
    volume = models.CharField(max_length=255)
    issues = models.TextField()
    copies = models.CharField(max_length=255)
    address1 = models.TextField()
    address2 = models.TextField(**dnb)
    remarks = models.TextField(**dnb)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"
