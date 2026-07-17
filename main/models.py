from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(verbose_name="IP Address")
    port = models.PositiveIntegerField(default=80)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(User,  related_name="devices", on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="devices/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    devices = models.ManyToManyField(Device, related_name="rooms", blank=True)

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", related_name="objs", on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    rooms = models.ManyToManyField(Room, related_name="floors")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name