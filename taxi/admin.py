from django.contrib import admin
from .models import User, Driver

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("login", "lname", "fname", "phone", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("login", "lname", "fname", "phone")

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("lname", "fname", "phone", "car_model", "car_number", "status", "is_blacklist")
    list_filter = ("status", "is_blacklist")
    search_fields = ("lname", "fname", "phone", "car_model", "car_number")