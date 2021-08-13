from urllib.parse import urlencode
from django.http.response import HttpResponseBase


class UpMiddleware:
    """
    Implements the Unpoly server protocol as described at https://unpoly.com/up.protocol
    """
    exclude_redirect_headers = ('X-Up-Method',)

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_up_headers(self, response):
        return [(header, value) for header, value in response.items() if header.startswith('X-Up-')]

    def _get_up_redirect_headers(self, response):
        return [(x, y) for x, y in self._get_up_headers(response) if x not in self.exclude_redirect_headers]

    def _get_up_params(self, request):
        return [(header, value) for header, value in request.GET.items() if header.startswith('X-Up-')]

    def _handle_redirect_headers(self, response: HttpResponseBase):
        """
        Preserves Unpoly X-Up-Headers over redirects by adding them as GET parameters
        See https://github.com/jwaschkau/django-unpoly/issues/4
        """
        if not hasattr(response, 'url'):
            # Some responses do not have a url e.g. HttpResponseNotModified
            return response
        response['X-Up-Location'] = response.url  # Report the original url to Unpoly
        params = {}
        for header, value in self._get_up_redirect_headers(response):
            params[header] = response[header]
        if params:
            separator = '?' if '?' not in response.url else '&'
            response['Location'] += separator + urlencode(params)
        return response

    def _remove_up_params(self, GET, up_params):
        parameters = GET.copy()
        for param, value in up_params:
            del parameters[param]
        return parameters

    def __call__(self, request):
        # Save Unpoly parameters for later use and clean them up
        up_params = self._get_up_params(request)
        # Remove Up-Parameters sent by GET so they do not show up
        request.GET = self._remove_up_params(request.GET, up_params)

        response: HttpResponseBase = self.get_response(request)

        response["X-Up-Method"] = request.method

        # Redirect detection for IE11
        response["X-Up-Location"] = request.get_full_path()

        # Signaling the initial request method
        if request.method == 'GET' and 'X-Up-Target' not in request:
            response.set_cookie('_up_method', request.method)
        else:
            response.delete_cookie('_up_method')

        # Redirect headers can not be read by Unpoly.
        # The headers are written to the url parameters and are sent back to Unpoly
        # with the redirect target response.
        for header, value in up_params:
            response[header] = value
        if response.status_code >= 300 and response.status_code < 400:
            # If this is a redirect add the Unpoly headers
            response = self._handle_redirect_headers(request, response)

        return response
