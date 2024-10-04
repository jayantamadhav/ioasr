from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from journals.models import Article

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # Add all your static URLs here
        return [
            ("core:home"),
            ("core:about"),
            ("core:submit-research"),
            ("core:contact"),
            ("core:submit-research"),
            ("core:privacy-policy"),
            ("core:refund-policy"),
            ("core:terms-and-conditions"),
            ("core:subscribe-newsletter"),
            ("core:journals"),
            ("core:news-list"),
            ("core:announcements-list"),
            ("core:join-as-editor"),
            ("core:join-as-reviewer"),
            ("core:hard-copy-order"),
            ("core:blog-list"),
        ]

    def location(self, item):
        if isinstance(item, tuple):
            view_name, *params = item
            return reverse(view_name, args=params)
        return reverse(item)
    
class ArticleSitemap(Sitemap):
    priority = 1
    changefreq = "daily"

    def items(self):
        return Article.objects.all()

    def location(self, item):
        return item.get_absolute_url()