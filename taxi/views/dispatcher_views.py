from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from taxi.models import User, Driver, Client, Shift
from django.contrib.auth import logout

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
    return render(request, "dispatcher/drivers_list.html", {"drivers": drivers})


@login_required
def dispatcher_clients(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)
    clients = Client.objects.all()
    return render(request, "dispatcher/clients_list.html", {"clients": clients})


@login_required
def dispatcher_shifts(request):
    if not hasattr(request.user, "role") or request.user.role != "dispatcher":
        return HttpResponse("Доступ запрещён", status=403)
    shifts = Shift.objects.all()
    return render(request, "dispatcher/shifts_list.html", {"shifts": shifts})


def index(request):
    return HttpResponse("Главная страница такси-проекта")