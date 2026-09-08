from django.contrib import admin
from django.urls import path
from taxi.views import (
    index, admin_panel, CustomLoginView, add_driver, add_client, add_user, edit_driver, edit_client, edit_shift,
    edit_user, toggle_driver_archive, toggle_user_archive, drivers_list, clients_list, users_list, shifts_list, add_shift,
    logout_view)

urlpatterns = [
    path("", index, name="index"),
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
]