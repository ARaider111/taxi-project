from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from taxi.utils import log_action


class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        user = form.get_user()

        if hasattr(user, "is_archive") and user.is_archive:
            form.add_error(None, "Пользователь находится в архиве и не может войти")
            return self.form_invalid(form)

        login_result = super().form_valid(form)

        log_action(
            user=user,
            action="LOGIN",
            description=f"Вход в систему: {user.login}",
            ip_address=self.request.META.get("REMOTE_ADDR"),
        )
        
        if hasattr(user, "role") and user.role == "admin":
            return redirect("admin_panel")

        if hasattr(user, "role") and user.role == "dispatcher":
            return redirect("dispatcher_dashboard")

        return redirect("index")


def logout_view(request):
    if request.user.is_authenticated:
        log_action(
            user=request.user,
            action="LOGOUT",
            description=f"Выход из системы: {request.user.login}",
            ip_address=request.META.get("REMOTE_ADDR"),
        )
    
    logout(request)
    return redirect("login")