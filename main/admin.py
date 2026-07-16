from django.contrib import admin
from main.models import Device, Room, Floor, Category


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "ip_address", "port", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "ip_address"]

admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Floor)
