import json
import requests
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from main.models import Device
from main.api.dashboard_views import visible_devices

class DeviceDashboardView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/devices.html"

    def list(self, request):
        devices = visible_devices(request.user)
        context = {"devices": devices}

        return Response(context)
