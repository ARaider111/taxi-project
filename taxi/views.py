from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import User, Driver, Client


class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        # Сначала выполняем стандартный логин
        login_result = super().form_valid(form)
        user = self.request.user

        # Явно проверяем роль и редиректим
        if hasattr(user, "role") and user.role == "admin":
            return redirect("dashboard")

        return redirect("index")


def index(request):
    return HttpResponse("Главная страница такси-проекта")


@login_required
def dashboard(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    return render(request, "dashboard.html")


@login_required
def drivers_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    drivers = Driver.objects.all()
    return render(request, "drivers_list.html", {"drivers": drivers})


@login_required
def clients_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    clients = Client.objects.all()
    return render(request, "clients_list.html", {"clients": clients})


@login_required
def users_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    users = User.objects.all()
    return render(request, "users_list.html", {"users": users})

@login_required
def add_driver(request):
    # Только для admin
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    if request.method == "POST":
        lname = request.POST.get("lname")
        fname = request.POST.get("fname")
        patronimyc = request.POST.get("patronimyc") or None
        phone = request.POST.get("phone")
        car_model = request.POST.get("car_model")
        car_number = request.POST.get("car_number")

        Driver.objects.create(
            lname=lname,
            fname=fname,
            patronimyc=patronimyc,
            phone=phone,
            car_model=car_model,
            car_number=car_number,
            status="Вне работы",
            is_blacklist=False,
        )
        return redirect("dashboard")

    return render(request, "add_driver.html")

@login_required
def edit_driver(request, driver_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    driver = Driver.objects.get(pk=driver_id)

    if request.method == "POST":
        driver.lname = request.POST.get("lname")
        driver.fname = request.POST.get("fname")
        driver.patronimyc = request.POST.get("patronimyc") or None
        driver.phone = request.POST.get("phone")
        driver.car_model = request.POST.get("car_model")
        driver.car_number = request.POST.get("car_number")
        driver.status = request.POST.get("status", driver.status)
        # чёрный список — чекбокс
        driver.is_blacklist = request.POST.get("is_blacklist") == "on"
        driver.save()
        return redirect("dashboard")

    return render(request, "edit_driver.html", {"driver": driver})

@login_required
def toggle_driver_archive(request, driver_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    driver = Driver.objects.get(pk=driver_id)
    driver.is_archive = not driver.is_archive  # переключаем
    driver.save()

    return redirect("dashboard")

@login_required
def add_client(request):
    # Только для admin
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    if request.method == "POST":
        lname = request.POST.get("lname")
        fname = request.POST.get("fname")
        patronimyc = request.POST.get("patronimyc") or None
        phone = request.POST.get("phone")

        Client.objects.create(
            lname=lname,
            fname=fname,
            patronimyc=patronimyc,
            phone=phone,
            is_blacklist=False,  # дефолт
        )
        return redirect("dashboard")

    return render(request, "add_client.html")

@login_required
def edit_client(request, client_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    client = Client.objects.get(pk=client_id)

    if request.method == "POST":
        client.lname = request.POST.get("lname")
        client.fname = request.POST.get("fname")
        client.patronimyc = request.POST.get("patronimyc") or None
        client.phone = request.POST.get("phone")
        client.is_blacklist = request.POST.get("is_blacklist") == "on"
        client.save()
        return redirect("dashboard")

    return render(request, "edit_client.html", {"client": client})


@login_required
def add_user(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        lname = request.POST.get("lname")
        fname = request.POST.get("fname")
        patronimyc = request.POST.get("patronimyc") or None
        phone = request.POST.get("phone")
        role = request.POST.get("role", "dispatcher")
        is_active = request.POST.get("is_active") == "on"

        User.objects.create_user(
            login=login,
            password=password,
            lname=lname,
            fname=fname,
            patronimyc=patronimyc,
            phone=phone,
            role=role,
            is_active=is_active,
        )
        return redirect("dashboard")

    return render(request, "add_user.html")


@login_required
def edit_user(request, user_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    user_obj = User.objects.get(pk=user_id)

    if request.method == "POST":
        user_obj.login = request.POST.get("login")
        user_obj.lname = request.POST.get("lname")
        user_obj.fname = request.POST.get("fname")
        user_obj.patronimyc = request.POST.get("patronimyc") or None
        user_obj.phone = request.POST.get("phone")
        user_obj.role = request.POST.get("role", user_obj.role)
        user_obj.is_active = request.POST.get("is_active") == "on"

        # Если ввели новый пароль — обновляем
        new_password = request.POST.get("password")
        if new_password:
            user_obj.set_password(new_password)

        user_obj.save()
        return redirect("dashboard")

    return render(request, "edit_user.html", {"user_obj": user_obj})

@login_required
def toggle_user_archive(request, user_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    user_obj = User.objects.get(pk=user_id)
    user_obj.is_archive = not user_obj.is_archive
    user_obj.save()

    return redirect("dashboard")
