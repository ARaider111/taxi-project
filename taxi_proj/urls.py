from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from taxi.views import (index, dashboard, CustomLoginView, add_driver, add_client, 
edit_driver, edit_client, toggle_driver_archive, add_user, edit_user, toggle_user_archive)
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
    path("dashboard/", dashboard, name="dashboard"),
    path("drivers/add/", add_driver, name="add_driver"),
    path("clients/add/", add_client, name="add_client"),
    path("users/add/", add_user, name="add_user"),
    path("drivers/<int:driver_id>/edit/", edit_driver, name="edit_driver"),
    path("clients/<int:client_id>/edit/", edit_client, name="edit_client"),
    path("users/<int:user_id>/edit/", edit_user, name="edit_user"),
    path("drivers/<int:driver_id>/toggle-archive/", toggle_driver_archive, name="toggle_driver_archive"),
    path("users/<int:user_id>/toggle-archive/", toggle_user_archive, name="toggle_user_archive"),
]