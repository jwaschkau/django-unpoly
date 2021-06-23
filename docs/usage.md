# Usage

To use django-unpoly in a project

```python
MIDDLEWARE = [
...
'django_unpoly.middleware.UpMiddleware',
...
]
```

## Unpoly Modal forms

The target is determined automatically if the model uses the `UpModelIdMixin` and updated
if the successful form submission returns html containing `up-id`. Form errors will update
the current open modal dialog.

### Python

```python
from django_unpoly.up import UpViewMixin
from django.views.generic import UpdateView

class MyUnpolyModelView(UpModelViewMixin, UpdateView):
    autosubmit = True
    form_class = MyFormClass
    template_name = 'django_unpoly/form.up.html'
    model = MyModel
```

### HTML

```html
<div up-id="{{object.up_id}}">
    <a up-layer="new" href="{% url 'myformurl' object.id %}">
        MyModal
    </a>
</div>
```

A redirect may be used to update the target on successful form submissions.

```html
<div up-id="{{object.up_id}}">
    <a up-layer="new" href="{% url 'myformurl' object.id %}?redirect="currentpage">
        MyModal
    </a>
</div>
```

## django-debug-toolbar

In your main layout include the following js-file.
```html
<script src="{% static 'django_unpoly/up_djdt.js' %}"></script>
```

# django-concurrency

The current version of the model has to be added to the unpoly form url. Before the form is rendered the
version will be checked for changes. The `version` field should also be added to the form to prevent
concurrent changes to the model.

```html
<a up-modal="new" href="{% url 'myurl' model.id %}?version={{ model.version }}">
    MyModal
</a>
```

```python
from django_unpoly.up import UpModelViewMixin, UpDjangoConcurrencyMixin
from django.views.generic import UpdateView

class MyUnpolyModelView(UpDjangoConcurrencyMixin, UpModelViewMixin, UpdateView):
    autosubmit = True
    form_class = MyFormClass
    template_name = 'django_unpoly/form.unpoly.html'
    model = MyModel
```
