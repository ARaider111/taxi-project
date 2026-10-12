from django.contrib import admin
from django.urls import path
from taxi.views.auth_views import (CustomLoginView, logout_view)
from taxi.views import (
    admin_panel,)
from taxi.views.dispatcher_views import (
    dispatcher_dashboard, drivers_list, clients_list, add_client, shifts_list, add_shift,  audit_logs_list,
    edit_client,  dispatcher_open_shift, dispatcher_close_shift,  orders_list, dispatcher_add_order, edit_order,
    dispatcher_assign_driver, dispatcher_complete_order,  districts_list, edit_district, 
    add_district, streets_list, add_street, edit_street, tariffs_list, add_tariff, edit_tariff, toggle_tariff_archive, add_driver, edit_driver,
    toggle_driver_blacklist, toggle_driver_archive, toggle_client_blacklist, edit_shift)
from taxi.views.report_views import (orders_report_page, export_orders_report, drivers_report_page, dispatcher_shift_report, export_dispatcher_shift_report,
    export_drivers_report, clients_report_page,  export_clients_report, shifts_report_page, export_shifts_report, export_revenue_report, 
    revenue_report_page, audit_report_page, export_audit_report)


urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    
    path("admin/", admin_panel, name="admin_panel"),   
    path("shifts/add/", add_shift, name="add_shift"),
    
    path("shifts-report/", shifts_report_page, name="shifts_report_page"),
    path("shifts-report/export/", export_shifts_report, name="export_shifts_report"),

    

    

    path("orders/", orders_list, name="orders_list"),
    path("orders/<int:order_id>/edit/", edit_order, name="edit_order"),
    path("orders-report/", orders_report_page, name="orders_report_page"),
    path("orders-report/export/", export_orders_report, name="export_orders_report"),

    path("revenue-report/", revenue_report_page, name="revenue_report_page"),
    path("revenue-report/export/", export_revenue_report, name="export_revenue_report"),

    path("dashboard/", dispatcher_dashboard, name="dispatcher_dashboard"),
    path("dashboard/drivers/", drivers_list, name="drivers_list"),
    path("dashboard/drivers/add/", add_driver, name="add_driver"),
    path("dashboard/drivers/<int:driver_id>/edit/", edit_driver, name="edit_driver"),
    path("dashboard/drivers/<int:driver_id>/toggle-archive/", toggle_driver_archive, name="toggle_driver_archive"),
    path("dashboard/drivers/<int:driver_id>/toggle-blacklist/", toggle_driver_blacklist, name="toggle_driver_blacklist",),
    path("dashboard/drivers-report/", drivers_report_page, name="drivers_report_page"),
    path("dashboard/drivers-report/export/", export_drivers_report, name="export_drivers_report"),

    path("dashboard/clients/", clients_list, name="clients_list"),
    path("dashboard/clients/add/", add_client, name="add_client"),
    path("dashboard/clients/<int:client_id>/edit/", edit_client, name="edit_client"),
    path("dashboard/clients/<int:client_id>/toggle-blacklist/", toggle_client_blacklist, name="toggle_client_blacklist",),
    path("dashboard/clients-report/", clients_report_page, name="clients_report_page"),
    path("dashboard/clients-report/export/", export_clients_report, name="export_clients_report"),

    path("dashboard/shifts/", shifts_list, name="shifts_list"),
    path("dashboard/shifts/add/", add_shift, name="add_shift"),
    path("dashboard/shifts/<int:shift_id>/edit/", edit_shift, name="edit_shift"),
    path("dashboard/shifts/<int:shift_id>/open/", dispatcher_open_shift, name="dispatcher_open_shift",),
    path("dashboard/shifts/<int:shift_id>/close/", dispatcher_close_shift, name="dispatcher_close_shift",),
    path("dispatcher/shift-report/", dispatcher_shift_report, name="dispatcher_shift_report"),
    path("dispatcher/shift-report/export/", export_dispatcher_shift_report, name="export_dispatcher_shift_report"),

    path("dashboard/orders/", orders_list, name="orders_list"),
    path("dashboard/orders/add/", dispatcher_add_order, name="dispatcher_add_order"),
    path("dashboard/orders/<int:order_id>/edit/", edit_order, name="edit_order"),
    path("dashboard/orders/<int:order_id>/assign-driver/", dispatcher_assign_driver, name="dispatcher_assign_driver"),
    path("dashboard/orders/<int:order_id>/complete/", dispatcher_complete_order, name="dispatcher_complete_order"),

  
    path("dashboard/districts/", districts_list, name="districts_list"),
    path("dashboard/districts/add/", add_district, name="add_district"),
    path("dashboard/districts/<int:district_id>/edit/", edit_district, name="edit_district"),
    path("dashboard/streets/", streets_list, name="streets_list"),
    path("dashboard/streets/add/", add_street, name="add_street"),
    path("dashboard/streets/<int:street_id>/edit/", edit_street, name="edit_street"), 
    path("dashboard/tariffs/", tariffs_list, name="tariffs_list"),
    path("dashboard/tariffs/add/", add_tariff, name="add_tariff"),
    path("dashboard/tariffs/<int:tariff_id>/edit/", edit_tariff, name="edit_tariff"),
    path("dashboard/tariffs/<int:tariff_id>/toggle-archive/", toggle_tariff_archive, name="toggle_tariff_archive"),

    path("dashboard/audit-logs/", audit_logs_list, name="audit_logs_list"),
    path("dashboard/audit-report/", audit_report_page, name="audit_report_page"),
    path("dashboard/audit-report/export/", export_audit_report, name="export_audit_report"),
]