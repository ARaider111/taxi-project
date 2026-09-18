from django.contrib import admin
from django.urls import path
from taxi.views import (
     admin_panel, CustomLoginView, add_driver, add_client, add_user, edit_driver, edit_client, edit_shift,
    edit_user, toggle_driver_archive, toggle_user_archive, drivers_list, clients_list, users_list, shifts_list, add_shift,
    logout_view, districts_list, edit_district, add_district, streets_list, add_street, edit_street, toggle_driver_blacklist,
    toggle_client_blacklist, tariffs_list, add_tariff, edit_tariff, toggle_tariff_archive, edit_order, orders_list, audit_logs_list, orders_report_page,
    export_orders_report, dispatchers_report_page, export_dispatchers_report, drivers_report_page, export_drivers_report, clients_report_page,
    export_clients_report, shifts_report_page, export_shifts_report, export_revenue_report, revenue_report_page, audit_report_page, export_audit_report)
from taxi.views.dispatcher_views import (
     dispatcher_dashboard, dispatcher_drivers, dispatcher_clients, dispatcher_shifts, dispatcher_add_client,
    dispatcher_edit_client,  dispatcher_open_shift, dispatcher_close_shift,  dispatcher_orders_list, dispatcher_add_order, dispatcher_edit_order,
    dispatcher_assign_driver, dispatcher_complete_order)

urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    
    # Админ‑панель 
    path("admin/", admin_panel, name="admin_panel"),

    path("audit-logs/", audit_logs_list, name="audit_logs_list"),
    path("audit-report/", audit_report_page, name="audit_report_page"),
    path("audit-report/export/", export_audit_report, name="export_audit_report"),
    
    # Водители
    path("drivers/", drivers_list, name="drivers_list"),
    path("drivers/add/", add_driver, name="add_driver"),
    path("drivers/<int:driver_id>/edit/", edit_driver, name="edit_driver"),
    path("drivers/<int:driver_id>/toggle-archive/", toggle_driver_archive, name="toggle_driver_archive"),
    path("drivers/<int:driver_id>/toggle-blacklist/", toggle_driver_blacklist, name="toggle_driver_blacklist",),
    path("drivers-report/", drivers_report_page, name="drivers_report_page"),
    path("drivers-report/export/", export_drivers_report, name="export_drivers_report"),

    # Клиенты
    path("clients/", clients_list, name="clients_list"),
    path("clients/add/", add_client, name="add_client"),
    path("clients/<int:client_id>/edit/", edit_client, name="edit_client"),
    path("clients/<int:client_id>/toggle-blacklist/", toggle_client_blacklist, name="toggle_client_blacklist",),
    path("clients-report/", clients_report_page, name="clients_report_page"),
    path("clients-report/export/", export_clients_report, name="export_clients_report"),

    # Пользователи
    path("users/", users_list, name="users_list"),
    path("users/add/", add_user, name="add_user"),
    path("users/<int:user_id>/edit/", edit_user, name="edit_user"),
    path("users/<int:user_id>/toggle-archive/", toggle_user_archive, name="toggle_user_archive"),
    path("dispatchers-report/", dispatchers_report_page, name="dispatchers_report_page"),
    path("dispatchers-report/export/", export_dispatchers_report, name="export_dispatchers_report"),

    path("shifts/", shifts_list, name="shifts_list"),
    path("shifts/add/", add_shift, name="add_shift"),
    path("shifts/<int:shift_id>/edit/", edit_shift, name="edit_shift"),
    path("shifts-report/", shifts_report_page, name="shifts_report_page"),
    path("shifts-report/export/", export_shifts_report, name="export_shifts_report"),

    # Районы
    path("districts/", districts_list, name="districts_list"),
    path("districts/add/", add_district, name="add_district"),
    path("districts/<int:district_id>/edit/", edit_district, name="edit_district"),

    # Улицы
    path("streets/", streets_list, name="streets_list"),
    path("streets/add/", add_street, name="add_street"),
    path("streets/<int:street_id>/edit/", edit_street, name="edit_street"), 

    # Тарифы
    path("tariffs/", tariffs_list, name="tariffs_list"),
    path("tariffs/add/", add_tariff, name="add_tariff"),
    path("tariffs/<int:tariff_id>/edit/", edit_tariff, name="edit_tariff"),
    path("tariffs/<int:tariff_id>/toggle-archive/", toggle_tariff_archive, name="toggle_tariff_archive"),

    # Заказы
    path("orders/", orders_list, name="orders_list"),
    path("orders/<int:order_id>/edit/", edit_order, name="edit_order"),
    path("orders-report/", orders_report_page, name="orders_report_page"),
    path("orders-report/export/", export_orders_report, name="export_orders_report"),

    path("revenue-report/", revenue_report_page, name="revenue_report_page"),
    path("revenue-report/export/", export_revenue_report, name="export_revenue_report"),


    # Диспетчер
    path("dashboard/", dispatcher_dashboard, name="dispatcher_dashboard"),
    path("dashboard/drivers/", dispatcher_drivers, name="dispatcher_drivers"),
    path("dashboard/clients/", dispatcher_clients, name="dispatcher_clients"),
    path("dashboard/clients/add/", dispatcher_add_client, name="dispatcher_add_client"),
    path("dashboard/clients/<int:client_id>/edit/", dispatcher_edit_client, name="dispatcher_edit_client"),
    path("dashboard/shifts/", dispatcher_shifts, name="dispatcher_shifts"),
    path("dashboard/shifts/<int:shift_id>/open/", dispatcher_open_shift, name="dispatcher_open_shift",),
    path("dashboard/shifts/<int:shift_id>/close/", dispatcher_close_shift, name="dispatcher_close_shift",),
    path("dashboard/orders/", dispatcher_orders_list, name="dispatcher_orders_list"),
    path("dashboard/orders/add/", dispatcher_add_order, name="dispatcher_add_order"),
    path("dashboard/orders/<int:order_id>/edit/", dispatcher_edit_order, name="dispatcher_edit_order"),
    path("dashboard/orders/<int:order_id>/assign-driver/", dispatcher_assign_driver, name="dispatcher_assign_driver"),
    path("dashboard/orders/<int:order_id>/complete/", dispatcher_complete_order, name="dispatcher_complete_order"),
]