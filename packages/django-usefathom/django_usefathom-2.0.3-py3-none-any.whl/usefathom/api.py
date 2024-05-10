from typing import Optional

EVENTS_SESSION_KEY = "_fathom_events"


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
        events = request.session.pop(EVENTS_SESSION_KEY, dict())
        events.update({event: value})
        request.session[EVENTS_SESSION_KEY] = events
    except AttributeError:
        pass


def fetch(request):
    try:
        return request.session.pop(EVENTS_SESSION_KEY, dict())
    except AttributeError:
        return {}
