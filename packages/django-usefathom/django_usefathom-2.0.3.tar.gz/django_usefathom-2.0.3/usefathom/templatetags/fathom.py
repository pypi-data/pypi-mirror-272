from typing import Optional

from django import template

register = template.Library()


@register.inclusion_tag("usefathom/click.html")
def click_event(event: str, value: Optional[int] = None):
    return _set_context(event, value)


@register.inclusion_tag("usefathom/submit.html")
def submit_goal(event: str, value: Optional[int] = None):
    return _set_context(event, value)


def _set_context(event: str, value: Optional[int] = None):
    ret = dict(event=event)
    if value is not None:
        ret.update(value=value)
    return ret
