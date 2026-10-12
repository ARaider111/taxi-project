from functools import wraps

from django.http import HttpResponse


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Требуется авторизация", status=401)
        return view_func(request, *args, **kwargs)

    return wrapper