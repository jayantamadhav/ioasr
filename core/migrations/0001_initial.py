# Generated by Django 5.1.1 on 2024-09-22 06:30

import core.models.user
import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="About",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("show_in_footer", models.BooleanField(default=False)),
                ("heading", models.CharField(max_length=255)),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("heading", models.TextField(verbose_name="Heading")),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "application_for",
                    models.CharField(
                        choices=[("Editor", "Editor"), ("Reviewer", "Reviewer")],
                        default="Editor",
                        max_length=255,
                    ),
                ),
                ("email", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=255)),
                (
                    "spcialization",
                    models.TextField(blank=True, default=None, null=True),
                ),
                ("affiliation", models.TextField(blank=True, default=None, null=True)),
                ("publications", models.TextField(blank=True, default=None, null=True)),
                ("photo", models.ImageField(upload_to="applications")),
                ("result", models.FileField(upload_to="applications")),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.TextField(blank=True, default=None, null=True)),
                ("heading", models.TextField()),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "featured_image",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="blogs"
                    ),
                ),
                ("keywords", models.TextField(blank=True, default=None, null=True)),
                ("views", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField(verbose_name="Title")),
                (
                    "isbn_online",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "isbn_print",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "doi",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "doi_link",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                ("about", models.TextField(blank=True, default=None, null=True)),
                (
                    "pdf",
                    models.FileField(blank=True, default=None, null=True, upload_to=""),
                ),
                (
                    "flyer",
                    models.FileField(blank=True, default=None, null=True, upload_to=""),
                ),
                (
                    "cover",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="book-covers"
                    ),
                ),
                (
                    "price",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "format",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                ("published", models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="FooterKeyword",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "keyword",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="Keyword",
                    ),
                ),
                ("link", models.TextField(blank=True, default=None, null=True)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Footer Keywords",
                "verbose_name_plural": "Footer Keywords",
            },
        ),
        migrations.CreateModel(
            name="HardCopyOrder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=255)),
                ("journal", models.CharField(max_length=255)),
                ("volume", models.CharField(max_length=255)),
                ("issues", models.TextField()),
                ("copies", models.CharField(max_length=255)),
                ("address1", models.TextField()),
                ("address2", models.TextField(blank=True, default=None, null=True)),
                ("remarks", models.TextField(blank=True, default=None, null=True)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Information",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("content", django_ckeditor_5.fields.CKEditor5Field()),
                (
                    "url",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("heading", models.TextField(verbose_name="Heading")),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "News",
                "verbose_name_plural": "News",
            },
        ),
        migrations.CreateModel(
            name="NewsletterSubscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=255,
                        null=True,
                        verbose_name="Email",
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="OfficeLocation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("address1", models.TextField(blank=True, default=None, null=True)),
                ("address2", models.TextField(blank=True, default=None, null=True)),
                (
                    "district",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "alt_phone",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "alt_email",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "office_hours",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "link",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Office Locations",
                "verbose_name_plural": "Office Locations",
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, default=None, max_length=31, null=True
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, default=None, max_length=31, null=True
                    ),
                ),
                (
                    "amount",
                    models.PositiveBigIntegerField(blank=True, default=None, null=True),
                ),
                (
                    "currency",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("remarks", models.TextField(blank=True, default=None, null=True)),
                ("rzp_order_id", models.CharField(max_length=255)),
                ("rzp_payment_id", models.CharField(max_length=255)),
                ("rzp_signature", models.CharField(max_length=255)),
                ("payment_verified", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="PublisherAdConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ad_space_1",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="ads"
                    ),
                ),
                (
                    "ad_space_1_link",
                    models.TextField(blank=True, default=None, null=True),
                ),
                (
                    "ad_space_2",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="ads"
                    ),
                ),
                (
                    "ad_space_2_link",
                    models.TextField(blank=True, default=None, null=True),
                ),
                (
                    "ad_space_3",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="ads"
                    ),
                ),
                (
                    "ad_space_3_link",
                    models.TextField(blank=True, default=None, null=True),
                ),
                (
                    "responsive_ad_space_1",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="ads"
                    ),
                ),
                (
                    "responsive_ad_space_1_link",
                    models.TextField(blank=True, default=None, null=True),
                ),
                (
                    "responsive_ad_space_2",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="ads"
                    ),
                ),
                (
                    "responsive_ad_space_2_link",
                    models.TextField(blank=True, default=None, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SiteConfiguration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="siteconfig"
                    ),
                ),
                ("site_name", models.CharField(default="Publisher", max_length=255)),
                (
                    "footer_copyright_label",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "about",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "contact_us",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "mission",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "vision",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "alt_email",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "alt_mobile",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "whatsapp",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("facebook", models.TextField(blank=True, default=None, null=True)),
                ("twitter", models.TextField(blank=True, default=None, null=True)),
                ("linkedin", models.TextField(blank=True, default=None, null=True)),
                ("youtube", models.TextField(blank=True, default=None, null=True)),
                ("academia_edu", models.TextField(blank=True, default=None, null=True)),
                (
                    "semantic_scholar",
                    models.TextField(blank=True, default=None, null=True),
                ),
                (
                    "google_scholar",
                    models.TextField(blank=True, default=None, null=True),
                ),
                ("maintenance_mode", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Site Configuration",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "first_name",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="profile_photo"),
                ),
                ("designation", models.TextField(blank=True, default=None, null=True)),
                ("institution", models.TextField(blank=True, default=None, null=True)),
                (
                    "achievements",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "publications",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, default=None, null=True
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("is_email_verified", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
            managers=[
                ("objects", core.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="BlogAuthor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                (
                    "last_name",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("profile_link", models.TextField(blank=True, default=None, null=True)),
                ("about", models.TextField(blank=True, default=None, null=True)),
                (
                    "profile_photo",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="blog_authors"
                    ),
                ),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_authors",
                        to="core.blog",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserEmailVerification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_verifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]