from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from main.permissions import IsAuthenticatedOrRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class ProfileView(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticatedOrRedirect]

    def get_permissions(self):
        if self.action == 'user_profile':
            return [permissions.AllowAny()]
        return [IsAuthenticatedOrRedirect()]

    def list(self, request):
        u = request.user
        ctx = {
            "profile_user": u,
            "device_count": u.devices.count(),
            "is_own_profile": True,
        }
        return Response(ctx, template_name='main/profile.html')

    @action(detail=True, methods=['get'], url_path='user_profile')
    def user_profile(self, request, username=None):
        u = get_object_or_404(User, username=username)
        ctx = {
            "profile_user": u,
            "device_count": u.devices.count(),
            "is_own_profile": request.user.is_authenticated and request.user.id == u.id,
        }
        return Response(ctx, template_name='main/user_profile.html')