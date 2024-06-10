import typing
from django.http.response import HttpResponseBase
from django.utils.translation import gettext as _

from django_unpoly.exceptions import UpException


class UpModelIdMixin:
    def up_id(self) -> str:
        return f"{self.__class__.__name__}_{self.pk}"


class UpMixin:

    # Unpoly Server protocol
    up_target: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Target
    up_clear_cache: typing.Union[str, None, typing.Callable] = '*'  # https://unpoly.com/X-Up-Clear-Cache
    up_accept_layer: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Accept-Layer
    up_dismiss_layer: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Dismiss-Layer
    up_events: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Events
    up_fail_mode: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Fail-Mode
    up_fail_target: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Fail-Target
    up_location: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/https://unpoly.com/X-Up-Location
    up_method: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Method
    up_reload_from_time: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Reload-From-Time
    up_title: typing.Union[str, None, typing.Callable] = None  # https://unpoly.com/X-Up-Title

    # Unpoly template
    layer: typing.Union[str, typing.Callable] = 'root'
    target: typing.Union[str, None, typing.Callable] = ':none'  # :none = Do not replace anyting on site

    def _get_value(self, attribute):
        if callable(attribute):
            return attribute()
        else:
            return attribute

    def _get_context_list(self) -> set:
        return {'target', 'layer', }

    def get_context_data(self, *args, **kwargs):
        for c in self._get_context_list():
            _attr = getattr(self, c)
            if _attr:
                kwargs.update({c: self._get_value(_attr)})

        return super().get_context_data(*args, **kwargs)

    def _get_dispatch_list(self) -> dict:
        return {
            'up_target': 'X-Up-Target',
            'up_clear_cache': 'X-Up-Clear-Cache',
            'up_accept_layer': 'X-Up-Accept-Layer',
            'up_dismiss_layer': 'X-Up-Dismiss-Layer',
            'up_events': 'X-Up-Events',
            'up_fail_mode': 'X-Up-Accept-Layer',
            'up_fail_target': 'X-Up-Fail-Target',
            'up_location': 'X-Up-Location',
            'up_method': 'X-Up-Method',
            'up_reload_from_time': 'X-Up-Reload-From-Time',
            'up_title': 'X-Up-Title',
        }

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        for _, up_key in self._get_dispatch_list().items():
            _attr = getattr(self, _)
            if _attr:
                response[up_key] = self._get_value(_attr)
        return response


class UpFormMixin(UpMixin):
    autosubmit: bool = False

    def form_invalid(self, *args, **kwargs):
        # Signaling failed form submissions
        # https://unpoly.com/up.protocol
        response: HttpResponseBase = super().form_invalid(*args, **kwargs)
        response.status_code = 422
        return response

    def _get_context_list(self):
        return super()._get_context_list().union({'autosubmit', })

    def get_success_url(self, *args, **kwargs):
        if 'redirect' in self.request.GET:
            return self.request.GET.get('redirect')
        else:
            return super().get_success_url(*args, **kwargs)

class UpDjangoConcurrencyMixin(UpMixin):
    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        # If the object uses a version field it has to be checked on first render
        if hasattr(self.object, "version"):
            if not self.request.GET.get("version", None):
                raise UpException(_("No version was passed to the form."))
            if self.request.GET.get("version") != str(self.object.version):
                raise UpException(
                    _("{object} was modified in another window.").format(
                        object=self.object._meta.verbose_name,
                        status_code=410
                    )
                )
        return result


class UpModelViewMixin(UpFormMixin):
    target: typing.Union[str, None, typing.Callable] = lambda self: f'*[up-id=\'{self.object.unpoly_id()}\']'
