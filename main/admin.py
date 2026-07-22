from django.contrib import admin
from main.models import Device, Room, Floor, Category


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "ip_address", "port", "is_active", "is_private", "is_semiprivate", "created_at"]
    list_filter = ["is_active", "is_private", "is_semiprivate"]
    search_fields = ["name", "ip_address"]
    fields = ["name", "ip_address", "port", "description", "is_active", "is_private", "is_semiprivate", "creator", "photo"]

admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Floor)
