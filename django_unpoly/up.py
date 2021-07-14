from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseBase
from django.utils.translation import gettext as _

from django_unpoly.exceptions import UpException


class UpModelIdMixin:
    def up_id(self):
        return f'{self.__class__.__name__}_{self.pk}'


class UpMixin:
    def __init__(self):
        self.up_target: Optional[str] = None  # if the up_target is set, it will be sent as X-Up-Target Request-Header

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if self.up_target:
            response['X-Up-Target'] = str(self.up_target)
        return response


class UpFormMixin(UpMixin):
    def form_invalid(self, *args, **kwargs):
        # Signaling failed form submissions
        # https://unpoly.com/up.protocol
        response: HttpResponseBase = super().form_invalid(*args, **kwargs)
        response.status_code = 422
        return response


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


class UpModelViewMixin(LoginRequiredMixin, UpFormMixin):
    autosubmit: bool = False

    def get_context_data(self, *args, **kwargs):
        if "target" not in kwargs:
            kwargs.update({"target": f"*[up-id='{self.object.up_id()}']"})
        if "autosubmit" not in kwargs:
            kwargs.update({"autosubmit": self.autosubmit})
        return super().get_context_data(*args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        try:
            return self.request.GET.get("redirect")
        except Exception:
            return super().get_success_url(*args, **kwargs)
