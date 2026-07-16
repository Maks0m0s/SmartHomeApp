from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from main.models import Device
from main.services.dashboard_service import (
    get_categories,
    get_floors,
    get_users,
    get_rooms_for_floor,
    get_devices_for_room,
    get_devices_for_user,
    get_devices_by_active_state,
    get_devices_by_inactive_state,
)


def _base_context():
    context = get_categories()
    context["floors"] = get_floors()
    context["users"] = get_users()
    context["active_count"] = get_devices_by_active_state().count()
    context["stopped_count"] = get_devices_by_inactive_state().count()
    context["selected_category"] = None
    context["selected_item"] = None
    context["devices"] = Device.objects.none()
    return context


class DashboardView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request):
        return Response(_base_context())

    def retrieve(self, request, pk=None):
        return Response(_base_context())


class FloorDevicesView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request, floor_id=None):
        context = _base_context()
        context["rooms"] = get_rooms_for_floor(floor_id)
        context["selected_category"] = "floors"
        context["selected_item"] = int(floor_id)
        return Response(context)

    def retrieve(self, request, floor_id=None, room_id=None):
        context = _base_context()
        context["rooms"] = get_rooms_for_floor(floor_id)
        context["devices"] = get_devices_for_room(room_id)
        context["selected_category"] = "floors"
        context["selected_item"] = int(room_id)
        return Response(context)


class FloorRoomsAPIView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def list(self, request, floor_id=None):
        rooms = get_rooms_for_floor(floor_id)
        data = [
            {
                "id": room.id,
                "name": room.name,
                "device_count": room.devices.count(),
            }
            for room in rooms
        ]
        return Response({"rooms": data})


class UserDevicesView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request, user_id=None):
        context = _base_context()
        context["devices"] = get_devices_for_user(user_id)
        context["selected_category"] = "person"
        context["selected_item"] = int(user_id)
        return Response(context)


class StateDevicesView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/dashboard.html"

    def list(self, request, state=None):
        context = _base_context()
        context["selected_category"] = "state"
        context["selected_item"] = state

        if state == "active":
            context["devices"] = get_devices_by_active_state()
        elif state == "stopped":
            context["devices"] = get_devices_by_inactive_state()
        else:
            context["devices"] = Device.objects.none()

        return Response(context)
