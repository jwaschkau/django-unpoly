# Usage

To use django-unpoly in a project

```python
MIDDLEWARE = [
...
'django_unpoly.middleware.UnpolyMiddleware',
...
]
```

## Unpoly forms

The target is determined automatically if the model uses the `UnpolyModelIdMixin`.

```python
from django_unpoly.up import UnpolyModelViewMixin
from django.views.generic import UpdateView

class MyUnpolyModelView(UnpolyModelViewMixin, UpdateView):
    autosubmit = True
    form_class = MyFormClass
    template_name = 'django_unpoly/form.unpoly.html'
    model = MyModel
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
version={model.version}
<a up-modal="#main" href="{% url 'myurl' model.id %}?version={{ model.version }}">
    MyModal
</a>
```

```python
from django_unpoly.up import UnpolyModelViewMixin, DjangoConcurrencyMixin
from django.views.generic import UpdateView

class MyUnpolyModelView(DjangoConcurrencyMixin, UnpolyModelViewMixin, UpdateView):
    autosubmit = True
    form_class = MyFormClass
    template_name = 'django_unpoly/form.unpoly.html'
    model = MyModel
```
