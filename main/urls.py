from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from main.api.home_views import HomeViewSet
from main.api.device_views import DeviceDashboardView

router = DefaultRouter()

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path('devices/', DeviceDashboardView.as_view({'get':'list'}), name='device-dashboard'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
