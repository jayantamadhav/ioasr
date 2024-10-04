from django.contrib import admin

from journals.models import (
    Journal,
    EditorialBoard,
    Indexing,
    Article,
    ArticleSection,
    ArticleAuthor,
    Volume,
    Issue,
    Subject,
    Category,
    Policy,
)
from journals.models.archives import SpecialIssueGuestEditor
from journals.models.journal import JournalAdConfig


# Register your models here.
class JournalEditorialBoardInline(admin.TabularInline):
    model = EditorialBoard
    extra = 1
    classes = ("collapse",)


class JournalIndexingInline(admin.TabularInline):
    model = Indexing
    extra = 1
    classes = ("collapse",)


class JournalCategoriesInline(admin.TabularInline):
    model = Category
    extra = 1
    classes = ("collapse",)


class JournalAdConfigInline(admin.StackedInline):
    
    def has_add_permission(self, request, obj=None):
        journal = obj
        return not self.model.objects.filter(journal=journal).exists()
    
    model = JournalAdConfig
    extra = 1
    classes = ("collapse",)


class JournalAdmin(admin.ModelAdmin):
    model = Journal
    search_fields = ("name",)
    list_display = (
        "name",
        "abbreviation",
        "issn_online",
        "issn_print",
    )
    fieldsets = (
        (
            "Journal",
            {
                "fields": (
                    "name",
                    "abbreviation",
                    "subject",
                    "url",
                    "issn_print",
                    "issn_online",
                    "email",
                    "thumbnail",
                    "about",
                    "aim_and_scope",
                    "apc",
                    "cite_score",
                    "impact_factor",
                    "acceptance_rate",
                    "first_decision",
                    "acceptance_to_publication",
                    "review_time",
                    "logo",
                    "submission_link",
                )
            },
        ),
        (
            "Theme",
            {
                "fields": (
                    "primary_color",
                    "secondary_color",
                    "light_color",
                )
            },
        ),
    )
    inlines = [
        JournalEditorialBoardInline,
        JournalIndexingInline,
        JournalCategoriesInline,
        JournalAdConfigInline,
    ]


class ArticleSectionStackedInline(admin.StackedInline):
    model = ArticleSection
    extra = 5
    classes = [
        "collapse",
    ]


class ArticleAuthorTabularInline(admin.TabularInline):
    model = ArticleAuthor
    extra = 1
    classes = [
        "collapse",
    ]


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    inlines = [ArticleSectionStackedInline, ArticleAuthorTabularInline]
    list_display = (
        "title",
        "article_type",
        "get_journal",
        "get_volume",
        "get_issue",
    )  # "downloads", "views")
    search_fields = ("title",)
    list_per_page = 20
    list_filter = (
        "article_type",
        "published",
    )
    fieldsets = (
        (
            "Article",
            {
                "fields": (
                    "is_open_access",
                    "in_press",
                    "issue",
                    "url",
                    "article_type",
                    "title",
                    "doi",
                    "doi_link",
                    "pmid",
                    "pmid_link",
                    "abstract",
                    "page_from",
                    "page_to",
                    "keywords",
                    "how_to_cite",
                    "received",
                    "revised",
                    "accepted",
                    "published",
                    "available_on",
                    "downloads",
                    "views",
                    "pdf",
                    "xml",
                    "auto_generate_pdf",
                    "auto_generate_xml"
                )
            },
        ),
        ("Citations", {"fields": ("apa", "mla", "chicago", "harvard", "vancouver")}),
    )

    @admin.display(description="Journal")
    def get_journal(self, obj):
        return obj.issue.volume.journal.name

    @admin.display(description="Volume")
    def get_volume(self, obj):
        return obj.issue.volume.name

    @admin.display(description="Issue")
    def get_issue(self, obj):
        return obj.issue.name


class SpecialIssueGuestEditorInlineAdmin(admin.TabularInline):
    model = SpecialIssueGuestEditor
    extra = 1
    classes = ("collapse",)


class IssueAdmin(admin.ModelAdmin):
    model = Issue
    list_display = (
        "name",
        "volume",
        "is_special_issue",
        "in_press",
    )
    fieldsets = (
        ("Standard Issue", {"fields": ("in_press", "volume", "name", "month")}),
        (
            "Special Issue",
            {
                "description": "Only fill up this form if this issue is a Special Issue",
                "fields": (
                    "is_special_issue",
                    "title",
                    "about",
                    "thumbnail",
                    "submission_deadline",
                    "is_published",
                    "published",
                ),
            },
        ),
    )
    inlines = [SpecialIssueGuestEditorInlineAdmin]

class PolicyAdmin(admin.ModelAdmin):
    model = Policy
    list_display = ("name", "journal")
    search_fields = ("name", )


admin.site.register(Journal, JournalAdmin)
admin.site.register(Volume)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Subject)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Article, ArticleAdmin)
