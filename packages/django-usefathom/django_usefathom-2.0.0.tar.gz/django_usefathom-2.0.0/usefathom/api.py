from typing import Optional
import json
import logging

from django.conf import settings


log = logging.getLogger(__name__)


def track(request, event: str, value: Optional[int] = None):
    """Track Fathom events

    Args:
        request ([type]): HttpRequest
        goal (str): Fathom events
        value (int, optional): Monetary value attached to event. Defaults to None.

    Raises:
        TypeError: Passing something else than request

    Returns:
        None: does not return anything
    """
    try:
        events = request.session.get("_fathom_events", "{}")
        fathom_events = json.loads(events)
        fathom_events.update({event: value})
        request.session["_fathom_events"] = json.dumps(events)
    except AttributeError:
        pass


def fetch(request):
    try:
        events = request.session.pop("_fathom_events", "{}")
        return json.loads(events)
    except AttributeError:
        return {}
