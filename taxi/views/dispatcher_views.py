from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from taxi.models import User, Driver, Client, Shift
from django.contrib.auth import logout
from django.utils import timezone
from django.db.models import Q

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