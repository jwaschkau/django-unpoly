from django.http.response import HttpResponseBase


class UpMiddleware:
    """
    Implements the unpoly server protocol as described at https://unpoly.com/up.protocol
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: HttpResponseBase = self.get_response(request)

        response["X-Up-Method"] = request.method

        # Redirect detection for IE11
        response["X-Up-Location"] = request.get_full_path()

        # Signaling the initial request method
        if request.method == "GET" and "X-Up-Target" not in request:
            response.set_cookie("_up_method", request.method)
        else:
            response.delete_cookie("_up_method")

        return response
