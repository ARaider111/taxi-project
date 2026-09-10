from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from taxi.models import User, Driver, Client, Shift
from django.contrib.auth import logout
from django.db.models import Q

class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        login_result = super().form_valid(form)
        user = self.request.user

        if hasattr(user, "role") and user.role == "admin":
            return redirect("admin_panel")

        if hasattr(user, "role") and user.role == "dispatcher":
            return redirect("dispatcher_dashboard")

        return redirect("index")


@login_required
def admin_panel(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    return render(request, "admin_panel.html")


@login_required
def drivers_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    drivers = Driver.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        drivers = drivers.filter(
            Q(lname__icontains=query) |
            Q(fname__icontains=query) |
            Q(phone__icontains=query) |
            Q(car_model__icontains=query) |
            Q(car_number__icontains=query)
        )

    status = request.GET.get("status", "")
    if status:
        drivers = drivers.filter(status=status)

    blacklist = request.GET.get("blacklist", "")
    if blacklist == "1":
        drivers = drivers.filter(is_blacklist=True)
    elif blacklist == "0":
        drivers = drivers.filter(is_blacklist=False)

    archive = request.GET.get("archive", "")
    if archive == "1":
        drivers = drivers.filter(is_archive=True)
    elif archive == "0":
        drivers = drivers.filter(is_archive=False)

    statuses = Driver.STATUS_CHOICES

    return render(request, "drivers_list.html", {
        "drivers": drivers,
        "statuses": statuses,
        "query": query,
        "current_status": status,
        "current_blacklist": blacklist,
        "current_archive": archive,
    })


@login_required
def clients_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    clients = Client.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        clients = clients.filter(
            Q(lname__icontains=query) |
            Q(fname__icontains=query) |
            Q(phone__icontains=query)
        )

    blacklist = request.GET.get("blacklist", "")
    if blacklist == "1":
        clients = clients.filter(is_blacklist=True)
    elif blacklist == "0":
        clients = clients.filter(is_blacklist=False)

    return render(request, "clients_list.html", {
        "clients": clients,
        "query": query,
        "current_blacklist": blacklist,
    })


@login_required
def users_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    users = User.objects.all()

    # Поиск по логину, фамилии, имени, отчеству, телефону
    query = request.GET.get("q", "").strip()
    if query:
        users = users.filter(
            Q(login__icontains=query) |
            Q(lname__icontains=query) |
            Q(fname__icontains=query) |
            Q(patronimyc__icontains=query) |
            Q(phone__icontains=query)
        )

    role = request.GET.get("role", "")
    if role:
        users = users.filter(role=role)

    is_active = request.GET.get("is_active", "")
    if is_active == "1":
        users = users.filter(is_active=True)
    elif is_active == "0":
        users = users.filter(is_active=False)

    archive = request.GET.get("archive", "")
    if archive == "1":
        users = users.filter(is_archive=True)
    elif archive == "0":
        users = users.filter(is_archive=False)

    roles = User.objects.values_list("role", flat=True).distinct()

    return render(request, "users_list.html", {
        "users": users,
        "roles": roles,
        "query": query,
        "current_role": role,
        "current_is_active": is_active,
        "current_archive": archive,
    })


@login_required
def shifts_list(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    shifts = Shift.objects.select_related(
        "driver", "opened_user", "closed_user"
    ).order_by("-start_shift")

    query = request.GET.get("q", "").strip()
    if query:
        shifts = shifts.filter(
            Q(driver__lname__icontains=query) |
            Q(driver__fname__icontains=query) |
            Q(start_shift__icontains=query) |
            Q(end_shift__icontains=query)
        )

    status = request.GET.get("status", "")
    if status == "not_opened":
        shifts = shifts.filter(opened_user__isnull=True)
    elif status == "opened":
        shifts = shifts.filter(
            opened_user__isnull=False,
            closed_user__isnull=True
        )
    elif status == "closed":
        shifts = shifts.filter(closed_user__isnull=False)

    return render(request, "shifts_list.html", {
        "shifts": shifts,
        "query": query,
        "current_status": status,
    })
@login_required
def add_driver(request):
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
        return redirect("drivers_list")

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
        driver.is_blacklist = request.POST.get("is_blacklist") == "on"
        driver.save()
        return redirect("drivers_list")

    return render(request, "edit_driver.html", {"driver": driver})

@login_required
def toggle_driver_archive(request, driver_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    driver = Driver.objects.get(pk=driver_id)
    driver.is_archive = not driver.is_archive  
    driver.save()

    return redirect("drivers_list")

@login_required
def add_client(request):
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
            is_blacklist=False,  
        )
        return redirect("clients_list")

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
        return redirect("clients_list")

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
        return redirect("users_list")

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

        new_password = request.POST.get("password")
        if new_password:
            user_obj.set_password(new_password)

        user_obj.save()
        return redirect("users_list")

    return render(request, "edit_user.html", {"user_obj": user_obj})

@login_required
def toggle_user_archive(request, user_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    user_obj = User.objects.get(pk=user_id)
    user_obj.is_archive = not user_obj.is_archive
    user_obj.save()

    return redirect("users_list")



@login_required
def add_shift(request):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    if request.method == "POST":
        driver_id = request.POST.get("driver")
        start_shift = request.POST.get("start_shift")  
        end_shift = request.POST.get("end_shift")


        Shift.objects.create(
            driver_id=driver_id,
            start_shift=start_shift.replace("T", " "),
            end_shift=end_shift.replace("T", " "),
        )
        return redirect("shifts_list")

    drivers = Driver.objects.filter(is_archive=False)
    return render(request, "add_shift.html", {"drivers": drivers})


@login_required
def edit_shift(request, shift_id):
    if not hasattr(request.user, "role") or request.user.role != "admin":
        return HttpResponse("Доступ запрещён", status=403)

    shift = Shift.objects.get(pk=shift_id)

    if request.method == "POST":
        driver_id = request.POST.get("driver")
        start_shift = request.POST.get("start_shift")
        end_shift = request.POST.get("end_shift")
        closed_user_id = request.POST.get("closed_user") or None

        shift.driver_id = driver_id
        shift.start_shift = start_shift.replace("T", " ")
        shift.end_shift = end_shift.replace("T", " ")
        shift.closed_user_id = closed_user_id if closed_user_id else None
        shift.save()

        return redirect("shifts_list")

    drivers = Driver.objects.filter(is_archive=False)
    users = User.objects.filter(is_archive=False)
    return render(request, "edit_shift.html", {
        "shift": shift,
        "drivers": drivers,
        "users": users,
    })


def logout_view(request):
    logout(request)
    return redirect("login")