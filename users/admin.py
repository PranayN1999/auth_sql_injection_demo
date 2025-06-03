# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Organization

# users/admin.py
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ("username", "email", "organization", "date_joined")
    list_filter   = ("organization", "is_staff")
    search_fields = ("username", "email")

    fieldsets = (
        (None,            {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "first_name", "last_name")}),
        ("Organisation",  {"fields": ("organization",)}),
        ("Permissions",   {"fields": ("is_staff", "is_superuser",
                                      "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    actions = ["assign_iu_innovates", "assign_iu_health"]

    # quick one‑click helpers (totally optional)
    def assign_iu_innovates(self, request, qs):
        org, _ = Organization.objects.get_or_create(name="IU Innovates")
        qs.update(organization=org)
    assign_iu_innovates.short_description = "Assign IU Innovates"

    def assign_iu_health(self, request, qs):
        org, _ = Organization.objects.get_or_create(name="IU Health")
        qs.update(organization=org)
    assign_iu_health.short_description = "Assign IU Health"
