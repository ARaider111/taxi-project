from functools import wraps

from django.http import HttpResponse


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponse("Требуется авторизация", status=401)

            if request.user.role not in allowed_roles:
                return HttpResponse("Доступ запрещён", status=403)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


admin_required = role_required("admin")
dispatcher_required = role_required("dispatcher")