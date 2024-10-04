from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
from solo.models import SingletonModel

from core.utils import dnb

class PublisherAdConfig(SingletonModel):
    ad_space_1 = models.ImageField(upload_to="ads", **dnb)
    ad_space_1_link = models.TextField(**dnb)
    ad_space_2 = models.ImageField(upload_to="ads", **dnb)
    ad_space_2_link = models.TextField(**dnb)
    ad_space_3 = models.ImageField(upload_to="ads", **dnb)
    ad_space_3_link = models.TextField(**dnb)
    responsive_ad_space_1 = models.ImageField(upload_to="ads", **dnb)
    responsive_ad_space_1_link = models.TextField(**dnb)
    responsive_ad_space_2 = models.ImageField(upload_to="ads", **dnb)
    responsive_ad_space_2_link = models.TextField(**dnb)

    def __str__(self):
        return "Ad Configuration"

class SiteConfiguration(SingletonModel):
    logo = models.ImageField(upload_to="siteconfig",**dnb)
    site_name = models.CharField(max_length=255, default="Publisher")
    footer_copyright_label = models.CharField(max_length=255, **dnb)
    about = CKEditor5Field(**dnb)
    contact_us = CKEditor5Field(**dnb)
    mission = CKEditor5Field(**dnb)
    vision = CKEditor5Field(**dnb)
    email = models.CharField(max_length=255, **dnb)
    alt_email = models.CharField(max_length=255, **dnb)
    mobile = models.CharField(max_length=255, **dnb)
    alt_mobile = models.CharField(max_length=255, **dnb)
    whatsapp = models.CharField(max_length=255, **dnb)
    facebook = models.TextField(**dnb)
    twitter = models.TextField(**dnb)
    linkedin = models.TextField(**dnb)
    youtube = models.TextField(**dnb)
    academia_edu = models.TextField(**dnb)
    semantic_scholar = models.TextField(**dnb)
    google_scholar = models.TextField(**dnb)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
        
class OfficeLocation(models.Model):
    name = models.CharField(max_length=255, **dnb)
    address1 = models.TextField(**dnb)
    address2 = models.TextField(**dnb)
    district = models.CharField(max_length=255, **dnb)
    state = models.CharField(max_length=255, **dnb)
    country = models.CharField(max_length=255, **dnb)
    phone = models.CharField(max_length=255, **dnb)
    alt_phone = models.CharField(max_length=255, **dnb)
    email = models.CharField(max_length=255, **dnb)
    alt_email = models.CharField(max_length=255, **dnb)
    office_hours = models.CharField(max_length=255, **dnb)
    link = models.CharField(max_length=255, **dnb)
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Office Locations"
        verbose_name_plural = "Office Locations"