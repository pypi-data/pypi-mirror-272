from django.conf import settings

from .api import fetch


def usefathom(request):
    return {
        "fathom_events": fetch(request),
        "FATHOM_SITE_ID": settings.FATHOM_SITE_ID,
    }
