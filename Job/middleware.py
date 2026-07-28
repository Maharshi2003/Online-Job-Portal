from django.http import HttpResponseForbidden

class BlockAdminOnPort8000Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        port = request.get_port()

        if port == '8000' and request.path.startswith('/admin'):
            return HttpResponseForbidden("Admin not allowed")

        return self.get_response(request)