from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from taxi.views import (
    index, dashboard, CustomLoginView, add_driver, add_client, add_user, edit_driver, edit_client, 
    edit_user, toggle_driver_archive, toggle_user_archive, drivers_list, clients_list, users_list, )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),

    # Админ‑панель 
    path("dashboard/", dashboard, name="dashboard"),

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
]