from django.contrib import admin
from solo.admin import SingletonModelAdmin
from core.models import (
    SiteConfiguration,
    OfficeLocation,
    News,
    Announcement,
    About,
    Information,
    FooterKeyword,
    NewsletterSubscription,
    Blog,
    BlogAuthor,
    Membership,
    Member,
    MembershipApplication
)
from core.models.core import Application, HardCopyOrder
from core.models.payments import Payment
from core.models.site_config import PublisherAdConfig
from core.models.user import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class BlogAuthorInline(admin.TabularInline):
    model = BlogAuthor


class BlogAdmin(admin.ModelAdmin):
    model = Blog
    search_fields = ("heading",)
    readonly_fields = ("url",)
    list_display = (
        "heading",
        "created_at",
    )
    fieldsets = (
        (
            "Blog",
            {"fields": ("heading", "content", "keywords", "featured_image", "url")},
        ),
    )
    inlines = [BlogAuthorInline]


class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    list_display = ("email", "application_for", "created_at")


class HardCopyOrderAdmin(admin.ModelAdmin):
    model = HardCopyOrder
    list_display = ("email", "created_at")


class SiteConfigurationAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "logo",
                    "site_name",
                    "footer_copyright_label",
                    "about",
                    "mission",
                    "vision",
                    "contact_us",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "email",
                    "alt_email",
                    "mobile",
                    "alt_mobile",
                )
            },
        ),
        (
            "Social",
            {
                "fields": (
                    "facebook",
                    "twitter",
                    "linkedin",
                    "youtube",
                    "academia_edu",
                    "semantic_scholar",
                    "google_scholar",
                )
            },
        ),
    )


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "date_joined")
    ordering = ("date_joined",)
    readonly_fields = ("date_joined",)
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "photo",
                    "designation",
                    "institution",
                    "achievements",
                    "publications",
                )
            },
        ),
        # ... (other fieldsets)
        ("Change Password", {"fields": ("password",)}),
        (
            "Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                    "is_email_verified",
                    "is_active",
                    "is_superuser",
                    "is_staff",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "is_email_verified",
                ),
            },
        ),
    )

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ("rzp_order_id", "email", "amount", "currency",)
    search_fields = ("email", "rzp_order_id", "rzp_payment_id", "rzp_signature", )

class MembershipApplicationAdmin(admin.ModelAdmin):
    model = MembershipApplication
    list_display = ("email", "name", "membership_type", "created_at")
    search_fields = ("email", "name", "phone")

# Register your models here.
admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
admin.site.register(PublisherAdConfig, SingletonModelAdmin)
admin.site.register(OfficeLocation)
admin.site.register(News)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Announcement)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(HardCopyOrder, HardCopyOrderAdmin)
admin.site.register(Information)
admin.site.register(About)
admin.site.register(Membership)
admin.site.register(Member)
admin.site.register(FooterKeyword)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(NewsletterSubscription)
admin.site.register(Blog, BlogAdmin)
admin.site.register(User, UserAdmin)
