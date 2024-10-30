from django.urls import path
from core.views import *

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search", SearchView.as_view(), name="search"),
    path("error/", ErrorView.as_view(), name="error"),
    path("about-us/", AboutUsView.as_view(), name="about"),
    path("submit-research/", SubmitResearchView.as_view(), name="submit-research"),
    path("contact-us/", ContactUsView.as_view(), name="contact"),
    path("submit-research/", SubmitResearchView.as_view(), name="submit-research"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("refund-policy/", RefundPolicyView.as_view(), name="refund-policy"),
    path("terms-and-conditions/", TermsAndConditionsView.as_view(), name="terms-and-conditions"),
    path("subscribe-newsletter/", SubscribeNewsletterView.as_view(), name="subscribe-newsletter"),
    path("journals", BrowseJournalView.as_view(), name="journals"),
    path("news", NewsListView.as_view(), name="news-list"),
    path("news/<int:pk>/", NewsDetailsView.as_view(), name="news-details"),
    path("announcements", AnnouncementListView.as_view(), name="announcements-list"),
    path("announcements/<int:pk>/", AnnouncementDetailsView.as_view(), name="announcement-details"),
    path("information/<str:url>/", InformationDetailsView.as_view(), name="information-details"),
    path("join/editor/", JoinAsEditorView.as_view(), name="join-as-editor"),
    path("join/reviewer/", JoinAsReviewerView.as_view(), name="join-as-reviewer"),
    path("hard-copy-order/", HardCopyOrderView.as_view(), name="hard-copy-order"),
    
    # Blogs
    path("blogs/", BlogListView.as_view(), name="blog-list"),
    path("blogs/<str:url>/", BlogDetailsView.as_view(), name="blog-details"),

    # Payments
    path("payments/", PaymentView.as_view(), name="payments"),
    path("payments/callback/", PaymentCallbackView.as_view(), name="payments-callback"),
    path("payments/success/", PaymentSuccessView.as_view(), name="payments-success"),
    path("payments/failed/", PaymentFailedView.as_view(), name="payments-failed"),
    
    # Memberships
    path("membership/apply/", MembershipApplicationView.as_view(), name="membership-apply"),
    path("membership/<str:url>/", MembershipInfoView.as_view(), name="membership-info"),
]
