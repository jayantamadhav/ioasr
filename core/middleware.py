from django.shortcuts import redirect

class ErrorRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:  # Check for error status codes
            return redirect('core:error')
        return response