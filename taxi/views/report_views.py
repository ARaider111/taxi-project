from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, Q, Sum
from django.db.models import Func
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import datetime, timedelta

from taxi.models import AuditLog, Client, Driver, Order, Shift, User

from .helpers import admin_required
from taxi.views.excel_reports import (
    autofit_columns,
    create_workbook,
    workbook_response,
)

@login_required
@admin_required
def orders_report_page(request):

    drivers = Driver.objects.filter(is_archive=False)

    return render(request, "orders_report.html", {
        "drivers": drivers,
        "status_choices": Order.STATUS_CHOICES,
    })


@login_required
@admin_required
def export_orders_report(request):

    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")
    status_filter = request.GET.get("status", "")
    driver_filter = request.GET.get("driver", "")

    orders = Order.objects.select_related(
        "client", "driver", "tariff", "street_from", "street_to", "created_by"
    ).all()

    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)
    if status_filter:
        orders = orders.filter(status=status_filter)
    if driver_filter:
        orders = orders.filter(driver_id=driver_filter)

  
    headers = [
        "Номер заказа", "Дата создания", "Статус", "Клиент", "Телефон",
        "Водитель", "Авто", "Откуда", "Дом", "Куда", "Дом",
        "Тариф", "Цена", "Создал", "Время выполнения (мин)"
    ]

    workbook, worksheet = create_workbook("Заказы", headers)
    
    for order in orders:
        duration = ""
        if order.completed_at and order.created_at:
            duration = int((order.completed_at - order.created_at).total_seconds() / 60)

        worksheet.append([
            order.order_number,
            order.created_at.strftime("%d.%m.%Y %H:%M"),
            order.status,
            f"{order.client.lname} {order.client.fname}",
            order.client.phone,
            f"{order.driver.lname} {order.driver.fname}" if order.driver else "",
            f"{order.driver.car_model} {order.driver.car_number}" if order.driver else "",
            order.street_from.name,
            order.house_from,
            order.street_to.name,
            order.house_to,
            order.tariff.name,
            str(order.price),
            f"{order.created_by.lname} {order.created_by.fname}",
            duration,
        ])

    
    autofit_columns(worksheet)

    filename = f"orders_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return workbook_response(workbook, filename)


@login_required
@admin_required
def dispatchers_report_page(request):
    return render(request, "dispatchers_report.html", {
        "roles": User.ROLE_CHOICES,
    })


@login_required
@admin_required
def export_dispatchers_report(request):
    role_filter = request.GET.get("role", "")
    is_active_filter = request.GET.get("is_active", "")
    is_archive_filter = request.GET.get("is_archive", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    users = User.objects.filter(role="dispatcher")

    if role_filter:
        users = users.filter(role=role_filter)
    if is_active_filter == "1":
        users = users.filter(is_active=True)
    elif is_active_filter == "0":
        users = users.filter(is_active=False)
    if is_archive_filter == "1":
        users = users.filter(is_archive=True)
    elif is_archive_filter == "0":
        users = users.filter(is_archive=False)

    headers = [
        "ID",
        "Логин",
        "Фамилия",
        "Имя",
        "Отчество",
        "Телефон",
        "Роль",
        "Активен",
        "Архив",
        "Создано заказов",
        "Открыто смен",
        "Закрыто смен",
        "Последний вход",
    ]

    workbook, worksheet = create_workbook("Диспетчеры", headers)

    for user in users:
        orders_count = Order.objects.filter(created_by=user).count()
        opened_shifts = Shift.objects.filter(opened_user=user).count()
        closed_shifts = Shift.objects.filter(closed_user=user).count()

        last_login = (
            user.last_login.strftime("%d.%m.%Y %H:%M")
            if user.last_login
            else "—"
        )

        worksheet.append([
            user.user_id,
            user.login,
            user.lname,
            user.fname,
            user.patronimyc or "",
            user.phone,
            user.role,
            "Да" if user.is_active else "Нет",
            "Да" if user.is_archive else "Нет",
            orders_count,
            opened_shifts,
            closed_shifts,
            last_login,
        ])

    autofit_columns(worksheet)

    filename = (
        "dispatchers_report_"
        f"{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    return workbook_response(workbook, filename)


@login_required
@admin_required
def drivers_report_page(request):
    return render(request, "drivers_report.html", {
        "statuses": Driver.STATUS_CHOICES,
    })


@login_required
@admin_required
def export_drivers_report(request):
    status_filter = request.GET.get("status", "")
    is_blacklist_filter = request.GET.get("is_blacklist", "")
    is_archive_filter = request.GET.get("is_archive", "")

    drivers = Driver.objects.all()

    if status_filter:
        drivers = drivers.filter(status=status_filter)
    if is_blacklist_filter == "1":
        drivers = drivers.filter(is_blacklist=True)
    elif is_blacklist_filter == "0":
        drivers = drivers.filter(is_blacklist=False)
    if is_archive_filter == "1":
        drivers = drivers.filter(is_archive=True)
    elif is_archive_filter == "0":
        drivers = drivers.filter(is_archive=False)

    headers = [
        "ID",
        "Фамилия",
        "Имя",
        "Отчество",
        "Телефон",
        "Авто (модель)",
        "Авто (номер)",
        "Статус",
        "Чёрный список",
        "Архив",
        "Всего заказов",
        "Завершено заказов",
        "Выручка",
    ]

    workbook, worksheet = create_workbook("Водители", headers)

    drivers = drivers.annotate(
        total_orders=Count("orders", distinct=True),
        completed_orders=Count(
            "orders",
            filter=Q(orders__status="Завершен"),
            distinct=True,
        ),
        revenue=Sum(
            "orders__price",
            filter=Q(orders__status="Завершен"),
        ),
    )

    for driver in drivers:
        revenue = driver.revenue or 0

        worksheet.append([
            driver.driver_id,
            driver.lname,
            driver.fname,
            driver.patronimyc or "",
            driver.phone,
            driver.car_model,
            driver.car_number,
            driver.status,
            "Да" if driver.is_blacklist else "Нет",
            "Да" if driver.is_archive else "Нет",
            driver.total_orders,
            driver.completed_orders,
            str(revenue),
        ])

    autofit_columns(worksheet)

    filename = (
        "drivers_report_"
        f"{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    return workbook_response(workbook, filename)


@login_required
@admin_required
def clients_report_page(request):
    return render(request, "clients_report.html", {})


@login_required
@admin_required
def export_clients_report(request):
    is_blacklist_filter = request.GET.get("is_blacklist", "")
    min_orders = request.GET.get("min_orders", "")

    clients = Client.objects.all()

    if is_blacklist_filter == "1":
        clients = clients.filter(is_blacklist=True)
    elif is_blacklist_filter == "0":
        clients = clients.filter(is_blacklist=False)

    if min_orders and min_orders.isdigit():
        min_orders = int(min_orders)
        clients = clients.annotate(
            orders_count=Count("orders")
        ).filter(orders_count__gte=min_orders)

    headers = [
        "ID",
        "Фамилия",
        "Имя",
        "Отчество",
        "Телефон",
        "Чёрный список",
        "Всего заказов",
        "Последний заказ",
        "Общая сумма",
    ]

    workbook, worksheet = create_workbook("Клиенты", headers)

    for client in clients:
        total_orders = Order.objects.filter(client=client).count()

        last_order = (
            Order.objects
            .filter(client=client)
            .order_by("-created_at")
            .first()
        )
        last_order_date = (
            last_order.created_at.strftime("%d.%m.%Y %H:%M")
            if last_order
            else ""
        )

        total_amount = (
            Order.objects
            .filter(client=client, status="Завершен")
            .aggregate(total=Sum("price"))["total"]
            or 0
        )

        worksheet.append([
            client.client_id,
            client.lname,
            client.fname,
            client.patronimyc or "",
            client.phone,
            "Да" if client.is_blacklist else "Нет",
            total_orders,
            last_order_date,
            str(total_amount),
        ])

    autofit_columns(worksheet)

    filename = (
        "clients_report_"
        f"{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    return workbook_response(workbook, filename)


@login_required
@admin_required
def shifts_report_page(request):
    drivers = Driver.objects.filter(is_archive=False)

    return render(request, "shifts_report.html", {
        "drivers": drivers,
    })


@login_required
@admin_required
def export_shifts_report(request):
    driver_filter = request.GET.get("driver", "")

    shifts = Shift.objects.select_related("driver").all()

    if driver_filter:
        shifts = shifts.filter(driver__driver_id=driver_filter)

    headers = [
        "ID",
        "Водитель (ФИО)",
        "Водитель (телефон)",
        "Авто (модель)",
        "Авто (номер)",
        "Начало",
        "Конец",
        "Длительность (часы)",
    ]

    workbook, worksheet = create_workbook("Смены", headers)

    for shift in shifts:
        if shift.start_shift and shift.end_shift:
            duration = (
                (shift.end_shift - shift.start_shift).total_seconds() / 3600
            )
            duration_str = f"{duration:.1f}"
        else:
            duration_str = ""

        worksheet.append([
            shift.shift_id,
            f"{shift.driver.lname} {shift.driver.fname} {shift.driver.patronimyc or ''}",
            shift.driver.phone,
            shift.driver.car_model,
            shift.driver.car_number,
            (
                shift.start_shift.strftime("%d.%m.%Y %H:%M")
                if shift.start_shift
                else ""
            ),
            (
                shift.end_shift.strftime("%d.%m.%Y %H:%M")
                if shift.end_shift
                else ""
            ),
            duration_str,
        ])

    autofit_columns(worksheet)

    filename = (
        "shifts_report_"
        f"{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    return workbook_response(workbook, filename)


@login_required
@admin_required
def revenue_report_page(request):
    return render(request, "revenue_report.html", {})


@login_required
@admin_required
def export_revenue_report(request):
    period = request.GET.get("period", "day")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    orders = Order.objects.filter(status="Завершен")

    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            orders = orders.filter(created_at__gte=date_from_obj)
        except Exception:
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            date_to_obj = date_to_obj + timedelta(days=1)
            orders = orders.filter(created_at__lt=date_to_obj)
        except Exception:
            pass

    headers = [
        "Период",
        "Заказов",
        "Выручка",
        "Средний чек",
    ]

    workbook, worksheet = create_workbook("Доходы", headers)

    if period == "day":
        orders = (
            orders
            .annotate(
                period=Func(
                    models.F("created_at"),
                    function="DATE",
                    output_field=models.CharField(),
                )
            )
            .values("period")
            .annotate(
                orders_count=Count("order_id"),
                revenue=Sum("price"),
            )
            .order_by("period")
        )

        for row in orders:
            avg_check = (
                row["revenue"] / row["orders_count"]
                if row["orders_count"] > 0
                else 0
            )
            worksheet.append([
                row["period"],
                row["orders_count"],
                str(row["revenue"] or 0),
                f"{avg_check:.2f}",
            ])

    elif period == "month":
        orders = (
            orders
            .annotate(
                year=Func(
                    models.F("created_at"),
                    function="YEAR",
                    output_field=models.IntegerField(),
                ),
                month=Func(
                    models.F("created_at"),
                    function="MONTH",
                    output_field=models.IntegerField(),
                ),
            )
            .values("year", "month")
            .annotate(
                orders_count=Count("order_id"),
                revenue=Sum("price"),
            )
            .order_by("year", "month")
        )

        for row in orders:
            avg_check = (
                row["revenue"] / row["orders_count"]
                if row["orders_count"] > 0
                else 0
            )
            period_str = f"{row['month']:02d}.{row['year']}"
            worksheet.append([
                period_str,
                row["orders_count"],
                str(row["revenue"] or 0),
                f"{avg_check:.2f}",
            ])

    elif period == "year":
        orders = (
            orders
            .annotate(
                year=Func(
                    models.F("created_at"),
                    function="YEAR",
                    output_field=models.IntegerField(),
                )
            )
            .values("year")
            .annotate(
                orders_count=Count("order_id"),
                revenue=Sum("price"),
            )
            .order_by("year")
        )

        for row in orders:
            avg_check = (
                row["revenue"] / row["orders_count"]
                if row["orders_count"] > 0
                else 0
            )
            worksheet.append([
                str(row["year"]),
                row["orders_count"],
                str(row["revenue"] or 0),
                f"{avg_check:.2f}",
            ])

    else:
        total_orders = orders.count()
        total_revenue = orders.aggregate(total=Sum("price"))["total"] or 0
        avg_check = (
            total_revenue / total_orders
            if total_orders > 0
            else 0
        )

        worksheet.append([
            "Всего",
            total_orders,
            str(total_revenue),
            f"{avg_check:.2f}",
        ])

    autofit_columns(worksheet)

    filename = (
        "revenue_report_"
        f"{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    return workbook_response(workbook, filename)


@login_required
@admin_required
def audit_report_page(request):
    actions = AuditLog.ACTION_CHOICES
    users = User.objects.all()

    return render(request, "audit_report.html", {
        "actions": actions,
        "users": users,
    })


@login_required
@admin_required
def export_audit_report(request):
    action_filter = request.GET.get("action", "")
    user_filter = request.GET.get("user", "")
    object_type_filter = request.GET.get("object_type", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    audits = AuditLog.objects.select_related("user").all()

    if action_filter:
        audits = audits.filter(action=action_filter)
    if user_filter:
        audits = audits.filter(user__user_id=user_filter)
    if object_type_filter:
        audits = audits.filter(object_type__icontains=object_type_filter)
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            audits = audits.filter(created_at__gte=date_from_obj)
        except Exception:
            pass
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            date_to_obj = date_to_obj + timedelta(days=1)
            audits = audits.filter(created_at__lt=date_to_obj)
        except Exception:
            pass

    headers = [
        "ID",
        "Время",
        "Пользователь",
        "Действие",
        "Тип объекта",
        "ID объекта",
        "Описание",
        "Доп. данные",
        "IP",
    ]

    workbook, worksheet = create_workbook("Аудит", headers)

    for audit in audits:
        user_name = ""
        if audit.user:
            user_name = f"{audit.user.lname} {audit.user.fname}"
        else:
            user_name = "Система"

        extra_data = audit.extra_data or ""

        worksheet.append([
            audit.log_id,
            audit.created_at.strftime("%d.%m.%Y %H:%M:%S"),
            user_name,
            audit.get_action_display(),
            audit.object_type or "",
            audit.object_id or "",
            audit.description or "",
            extra_data[:500],
            audit.ip_address or "",
        ])

    autofit_columns(worksheet)

    filename = (
        "audit_report_"
        f"{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    return workbook_response(workbook, filename)