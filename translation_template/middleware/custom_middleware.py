from django.utils import translation


class UserLanguageMiddleware:
    """
    Used to load the User custom language in django-admin site
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.COOKIES:
            if request.COOKIES.get('django_language') == 'None':
                user = getattr(request, 'user', None)
                user_language = getattr(user, 'language', None)
                translation.activate(user_language)
                request.LANGUAGE_CODE = translation.get_language()
                response = self.get_response(request)
                response.set_cookie('django_language', user_language)
                return response

        if request.path.startswith('/admin/logout/'):
            user = getattr(request, 'user', None)
            user_language = getattr(user, 'language', None)
            response = self.get_response(request)
            response.set_cookie('django_language', user_language)
            return response
        return self.get_response(request)
