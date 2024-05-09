# django-usefathom

Fathom Analytics integration with Django projects. Provides ability to integrate
page view tracking and goal reporting.

> If you want to track goals instead of events, please use the 1.x.x version of the library.

## Installation

Install the package:

```
pip install django-usefathom
```

Add `usefathom` to your `settings.py` file:

```python
INSTALLED_APPS = [
    # ...
    "usefathom",
    # ...
]
```

Add template processor to your `settings.py` file:

```python
TEMPLATES = [
    {
        # ....
        "OPTIONS": {
            "context_processors": [
                # ...
                "usefathom.context_processors.usefathom",
                # ...
            ],
        },
    },
]
```

Add your fathom site id to your `settings.py` file:

```python
FATHOM_SITE_ID = "XXXX1234"
```

Include tracking snippet in your templates:

```jinja2
{% include "usefathom/usefathom.html" %}
```

From this point your site visits will be tracked.

## Event Tracking

### Python

Now if you want to report a event from your backend service to Fathom analytics:

```python
import usefathom

def some_view(request, *args, **kwargs):
    # anywhere you have request object, most likely views are a good place for this
    usefathom.track(request, "add_to_card", 100)  # Third parameter is optional integer, attaches the monetary value to the event in cents
```

And the goal will be reported to Fathom analytics on the next page load.

### HTML+JS

You can use template tags to track the goals from the html. It's useful when tracking external link clicks, etc.

```jinja2
{% load fathom }
......with link
<a href="https://go-somewhere.com/link" {% click_event "somewhere_link_clicked" 100 %}>Go somewhere?</a>
......with form
<form method="POST" {% submit_event "registration_submit" %}>
```

