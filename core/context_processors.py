from core.models import FooterKeyword


def footer_keywords(request):
    _keywords = FooterKeyword.objects.all()
    return {"footer_keywords": _keywords}
