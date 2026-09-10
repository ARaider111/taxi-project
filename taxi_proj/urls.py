from django.contrib import admin
from django.urls import path
from taxi.views import (
     admin_panel, CustomLoginView, add_driver, add_client, add_user, edit_driver, edit_client, edit_shift,
    edit_user, toggle_driver_archive, toggle_user_archive, drivers_list, clients_list, users_list, shifts_list, add_shift,
    logout_view)
from taxi.views.dispatcher_views import (
     dispatcher_dashboard, dispatcher_drivers, dispatcher_clients, dispatcher_shifts, dispatcher_add_client,
    dispatcher_edit_client,  dispatcher_open_shift, dispatcher_close_shift,
)

urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    
    # Админ‑панель 
    path("admin/", admin_panel, name="admin_panel"),

    # Водители
    path("drivers/", drivers_list, name="drivers_list"),
    path("drivers/add/", add_driver, name="add_driver"),
    path("drivers/<int:driver_id>/edit/", edit_driver, name="edit_driver"),
    path("drivers/<int:driver_id>/toggle-archive/", toggle_driver_archive, name="toggle_driver_archive"),

    # Клиенты
    path("clients/", clients_list, name="clients_list"),
    path("clients/add/", add_client, name="add_client"),
    path("clients/<int:client_id>/edit/", edit_client, name="edit_client"),

    # Пользователи
    path("users/", users_list, name="users_list"),
    path("users/add/", add_user, name="add_user"),
    path("users/<int:user_id>/edit/", edit_user, name="edit_user"),
    path("users/<int:user_id>/toggle-archive/", toggle_user_archive, name="toggle_user_archive"),

    path("shifts/", shifts_list, name="shifts_list"),
    path("shifts/add/", add_shift, name="add_shift"),
    path("shifts/<int:shift_id>/edit/", edit_shift, name="edit_shift"),


    # Диспетчер
    path("dashboard/", dispatcher_dashboard, name="dispatcher_dashboard"),
    path("dashboard/drivers/", dispatcher_drivers, name="dispatcher_drivers"),
    path("dashboard/clients/", dispatcher_clients, name="dispatcher_clients"),
    path("dashboard/clients/add/", dispatcher_add_client, name="dispatcher_add_client"),
    path("dashboard/clients/<int:client_id>/edit/", dispatcher_edit_client, name="dispatcher_edit_client"),
    path("dashboard/shifts/", dispatcher_shifts, name="dispatcher_shifts"),
    path("dashboard/shifts/<int:shift_id>/open/", dispatcher_open_shift, name="dispatcher_open_shift",),
    path("dashboard/shifts/<int:shift_id>/close/", dispatcher_close_shift, name="dispatcher_close_shift",),

]