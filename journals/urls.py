from django.urls import path
from journals.views import *

app_name = "journals"

urlpatterns = [
    path("download-article/pdf/", ArticleDownloadView.as_view(), name="article-download"),
    path("download-article/xml/<int:article_id>/", ArticleXMLDownloadView.as_view(), name="article-xml-download"),
    path("<str:url>/search", SearchView.as_view(), name="search"),
    path("<str:url>/about/<str:about_type>/", JournalAboutView.as_view(), name="about"),
    path("<str:url>/archives/", JournalArchiveListView.as_view(), name="archives"),
    path("<str:url>/archives/<str:vol>/<str:issue>/", JournalArchiveDetailsView.as_view(), name="archive-details"),
    path("<str:url>/insights", JournalInsightsView.as_view(), name="insights"),
    path("<str:url>/publications", JournalAuthorPublicationsView.as_view(), name="author-publications"),
    path("<str:url>/policy/<str:policy_url>/", JournalPolicyView.as_view(), name="policy"),

    # Special Issue
    path("<str:url>/special-issue/about/", JournalSpecialIssueAbout.as_view(), name="special-issue-about"),
    path("<str:url>/special-issue/propose/", JournalSpecialIssuePropose.as_view(), name="special-issue-propose"),
    path("<str:url>/special-issue/open/", JournalSpecialIssueOpen.as_view(), name="special-issue-open"),
    path("<str:url>/special-issue/published/", JournalSpecialIssuePublished.as_view(), name="special-issue-published"),
    path("<str:url>/special-issue/<str:vol>/<str:issue>/", JournalSpecialIssueDetails.as_view(), name="special-issue-details"),
    path("<str:url>/<str:vol>/<str:issue>/<str:article_url>/", JournalArticleView.as_view(), name="article"),
    path("<str:url>/", JournalDetailView.as_view(), name="home"),

]
