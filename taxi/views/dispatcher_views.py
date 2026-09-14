from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from taxi.models import User, Driver, Client, Shift, Street, Tariff, Order
from django.contrib.auth import logout
from django.utils import timezone
from django.db.models import Q
from django.db import models

@login_required
def dispatcher_dashboard(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)
    return render(request, "dispatcher/dashboard.html")


@login_required
def dispatcher_drivers(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
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

    statuses = Driver.STATUS_CHOICES  

    return render(request, "dispatcher/drivers_list.html", {
        "drivers": drivers,
        "statuses": statuses,
        "current_status": status,
        "query": query,
    })

@login_required
def dispatcher_clients(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)

    clients = Client.objects.all()

    query = request.GET.get("q", "").strip()
    if query:
        clients = clients.filter(
            Q(lname__icontains=query) |
            Q(fname__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(request, "dispatcher/clients_list.html", {
        "clients": clients,
        "query": query,
    })



def dispatcher_shifts(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
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

    return render(request, "dispatcher/shifts_list.html", {
        "shifts": shifts,
        "query": query,
        "current_status": status,
    })


@login_required
def dispatcher_add_client(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
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
        return redirect("dispatcher_clients")

    return render(request, "dispatcher/add_client.html")


@login_required
def dispatcher_edit_client(request, client_id):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)

    client = Client.objects.get(pk=client_id)

    if request.method == "POST":
        client.lname = request.POST.get("lname")
        client.fname = request.POST.get("fname")
        client.patronimyc = request.POST.get("patronimyc") or None
        client.phone = request.POST.get("phone")
        client.save()
        return redirect("dispatcher_clients")

    return render(request, "dispatcher/edit_client.html", {"client": client})

@login_required
def dispatcher_open_shift(request, shift_id):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)

    shift = Shift.objects.get(pk=shift_id)

    if shift.opened_user is None:
        shift.start_shift = timezone.now()
        shift.opened_user = request.user
        shift.save()

    return redirect("dispatcher_shifts")


@login_required
def dispatcher_close_shift(request, shift_id):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)

    shift = Shift.objects.get(pk=shift_id)

    if shift.opened_user is not None and shift.closed_user is None:
        shift.end_shift = timezone.now()
        shift.closed_user = request.user
        shift.save()

    return redirect("dispatcher_shifts")



@login_required
def dispatcher_orders_list(request):
    if not hasattr(request.user, "role") or request.user.role not in ["admin", "dispatcher"]:
        return HttpResponse("Доступ запрещён", status=403)

    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")

    orders = Order.objects.select_related(
        "client", "driver", "tariff", "street_from", "street_to", "created_by"
    ).all()

    if query:
        orders = orders.filter(
            models.Q(client__lname__icontains=query) |
            models.Q(client__fname__icontains=query) |
            models.Q(client__phone__icontains=query) |
            models.Q(order_number__icontains=query)
        )


    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        "orders": orders,
        "query": query,
        "current_status": status_filter,
        "status_choices": Order.STATUS_CHOICES,
    }

    return render(request, "dispatcher/orders_list.html", context)


@login_required
def dispatcher_add_order(request):
    if not hasattr(request.user, "role") or request.user.role not in ["admin", "dispatcher"]:
        return HttpResponse("Доступ запрещён", status=403)

    if request.method == "POST":
        client_id = request.POST.get("client")
        street_from_id = request.POST.get("street_from")
        house_from = request.POST.get("house_from")
        street_to_id = request.POST.get("street_to")
        house_to = request.POST.get("house_to")
        tariff_id = request.POST.get("tariff")

        client = Client.objects.get(pk=client_id)
        street_from = Street.objects.select_related("district").get(pk=street_from_id)
        street_to = Street.objects.select_related("district").get(pk=street_to_id)
        tariff = Tariff.objects.get(pk=tariff_id)

        coef_from = street_from.district.base_coefficient
        coef_to = street_to.district.base_coefficient
        price = tariff.price * ((coef_from + coef_to) / 2)

        order = Order.objects.create(
            client=client,
            street_from=street_from,
            house_from=house_from,
            street_to=street_to,
            house_to=house_to,
            tariff=tariff,
            price=price,
            created_by=request.user,
            status="Новый",
        )

        return redirect("orders_list")

   
    clients = Client.objects.all()
    streets = Street.objects.select_related("district").all()
    tariffs = Tariff.objects.filter(is_archive=False)

    return render(request, "dispatcher/add_order.html", {
        "clients": clients,
        "streets": streets,
        "tariffs": tariffs,
    })


@login_required
def dispatcher_edit_order(request, order_id):
    if not hasattr(request.user, "role") or request.user.role not in ["admin", "dispatcher"]:
        return HttpResponse("Доступ запрещён", status=403)

    order = Order.objects.select_related(
        "client", "driver", "tariff", "street_from", "street_to"
    ).get(pk=order_id)

    if order.status == "Завершен":
        return HttpResponse("Нельзя редактировать завершённый заказ", status=403)

    if request.method == "POST":
        client_id = request.POST.get("client")
        street_from_id = request.POST.get("street_from")
        house_from = request.POST.get("house_from")
        street_to_id = request.POST.get("street_to")
        house_to = request.POST.get("house_to")
        tariff_id = request.POST.get("tariff")

        order.client = Client.objects.get(pk=client_id)
        order.street_from = Street.objects.select_related("district").get(pk=street_from_id)
        order.house_from = house_from
        order.street_to = Street.objects.select_related("district").get(pk=street_to_id)
        order.house_to = house_to
        order.tariff = Tariff.objects.get(pk=tariff_id)

        coef_from = order.street_from.district.base_coefficient
        coef_to = order.street_to.district.base_coefficient
        order.price = order.tariff.price * ((coef_from + coef_to) / 2)

        order.save()
        return redirect("orders_list")

    clients = Client.objects.all()
    streets = Street.objects.select_related("district").all()
    tariffs = Tariff.objects.filter(is_archive=False)

    return render(request, "dispatcher/edit_order.html", {
        "order": order,
        "clients": clients,
        "streets": streets,
        "tariffs": tariffs,
    })


@login_required
def dispatcher_assign_driver(request, order_id):
    if not hasattr(request.user, "role") or request.user.role not in ["admin", "dispatcher"]:
        return HttpResponse("Доступ запрещён", status=403)

    order = Order.objects.get(pk=order_id)

    if order.status == "Завершен":
        return HttpResponse("Нельзя изменить завершённый заказ", status=403)

    if request.method == "POST":
        driver_id = request.POST.get("driver")
        driver = Driver.objects.get(pk=driver_id)

        order.driver = driver
        order.status = "Назначен водитель"
        order.save()

        return redirect("orders_list")

    drivers = Driver.objects.filter(status="В ожидании", is_blacklist=False, is_archive=False)

    return render(request, "dispatcher/assign_driver.html", {
        "order": order,
        "drivers": drivers,
    })



@login_required
def dispatcher_complete_order(request, order_id):
    if not hasattr(request.user, "role") or request.user.role not in ["admin", "dispatcher"]:
        return HttpResponse("Доступ запрещён", status=403)

    order = Order.objects.get(pk=order_id)

    if order.status == "Завершен":
        return HttpResponse("Заказ уже завершён", status=403)

    order.status = "Завершен"
    order.completed_at = timezone.now()
    order.save()

    return redirect("orders_list")