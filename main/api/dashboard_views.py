from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from main.models import Device, Category, Floor, Room


def _base_context():
    return {
        "categories": Category.objects.all(),
        "floors": Floor.objects.all().order_by("order"),
        "users": User.objects.all(),
        "active_count": Device.objects.filter(is_active=True).count(),
        "stopped_count": Device.objects.filter(is_active=False).count(),
        "selected_category": None,
        "selected_floor": None,
        "selected_room": None,
        "selected_user": None,
        "selected_state": None,
        "rooms": [],
        "devices": Device.objects.none(),
        "panel_title": '<i class="bi bi-grid-3x3-gap-fill me-2"></i>Devices',
        "panel_subtitle": "Select a category to view devices",
        "active_tab": "floors",
    }


class DashboardView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request):
        ctx = _base_context()
        ctx["devices"] = Device.objects.all()
        ctx["panel_subtitle"] = "All registered devices"
        return Response(ctx)


class FloorDetailView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request):
        ctx = _base_context()
        ctx["selected_category"] = "floors"
        return Response(ctx)

    def retrieve(self, request, floor_id=None):
        ctx = _base_context()
        floor = get_object_or_404(Floor, id=floor_id)
        ctx["selected_category"] = "floors"
        ctx["selected_floor"] = floor
        ctx["rooms"] = floor.rooms.all()
        ctx["devices"] = Device.objects.filter(rooms__in=floor.rooms.all()).distinct()
        ctx["panel_title"] = '<i class="bi bi-building me-2"></i>' + floor.name
        ctx["panel_subtitle"] = "All devices in " + floor.name
        return Response(ctx)


class RoomDetailView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request, floor_id=None):
        floor = get_object_or_404(Floor, id=floor_id)
        ctx = _base_context()
        ctx["selected_category"] = "floors"
        ctx["selected_floor"] = floor
        ctx["rooms"] = floor.rooms.all()
        return Response(ctx)

    def retrieve(self, request, floor_id=None, room_id=None):
        ctx = _base_context()
        floor = get_object_or_404(Floor, id=floor_id)
        room = get_object_or_404(Room, id=room_id)
        ctx["selected_category"] = "floors"
        ctx["selected_floor"] = floor
        ctx["selected_room"] = room
        ctx["rooms"] = floor.rooms.all()
        ctx["devices"] = room.devices.all()
        ctx["panel_title"] = '<i class="bi bi-door-open me-2"></i>' + room.name
        ctx["panel_subtitle"] = "Devices in " + room.name
        return Response(ctx)


class UserDetailView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request):
        ctx = _base_context()
        ctx["active_tab"] = "person"
        ctx["panel_subtitle"] = "Select a person to view their devices"
        return Response(ctx)

    def retrieve(self, request, user_id=None):
        ctx = _base_context()
        user_obj = get_object_or_404(User, id=user_id)
        ctx["active_tab"] = "person"
        ctx["selected_category"] = "person"
        ctx["selected_user"] = user_obj
        ctx["devices"] = Device.objects.filter(creator=user_obj)
        display_name = user_obj.get_full_name() or user_obj.username
        ctx["panel_title"] = '<i class="bi bi-person me-2"></i>' + display_name
        ctx["panel_subtitle"] = "Devices owned by " + display_name
        ctx["panel_is_user_profile"] = True
        return Response(ctx)


class StateDetailView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request):
        ctx = _base_context()
        ctx["active_tab"] = "state"
        ctx["panel_subtitle"] = "Select a state to view devices"
        return Response(ctx)

    def retrieve(self, request, state=None):
        ctx = _base_context()
        ctx["selected_category"] = "state"
        ctx["selected_state"] = state
        ctx["active_tab"] = "state"
        if state == "active":
            ctx["devices"] = Device.objects.filter(is_active=True)
            ctx["panel_title"] = '<i class="bi bi-check-circle me-2"></i>Active'
            ctx["panel_subtitle"] = "All active devices"
        elif state == "stopped":
            ctx["devices"] = Device.objects.filter(is_active=False)
            ctx["panel_title"] = '<i class="bi bi-x-circle me-2"></i>Stopped'
            ctx["panel_subtitle"] = "All stopped devices"
        else:
            ctx["devices"] = Device.objects.none()
        return Response(ctx)
