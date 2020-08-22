import os


class ServerURLWithStagingPortMiddlware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.environ.get("STAGING_PORT") and request.META.get("HTTP_HOST", None):
            request.META["HTTP_HOST"] = "{}:{}".format(
                request.META["HTTP_HOST"], os.environ["STAGING_PORT"]
            )
        response = self.get_response(request)
        return response
