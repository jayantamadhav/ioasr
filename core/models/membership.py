import re
import uuid
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from core.utils import dnb
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _


class Membership(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, **dnb)
    about = CKEditor5Field()
    eligibity_criteria = CKEditor5Field(**dnb)
    membership_benefits = CKEditor5Field(**dnb)
    certificate = models.ImageField(upload_to="memberships", **dnb)
    banner = models.ImageField(upload_to="memberships", **dnb)

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        sanitized_name = slugify(self.name)
        self.url = re.sub(r'-+', '-', sanitized_name)

        super().save(*args, **kwargs)


class Member(models.Model):
    membership = models.ForeignKey(
        Membership, on_delete=models.CASCADE, related_name="members"
    )
    name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255, **dnb)
    institution = models.CharField(max_length=255, **dnb)
    affiliation = models.CharField(max_length=255, **dnb)
    image = models.ImageField(upload_to="members", **dnb)

    def __str__(self):
        return f"{self.name}"
