from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from main.api.home_views import HomeViewSet
from main.api.dashboard_views import (
    DashboardView,
    FloorDevicesView,
    FloorRoomsAPIView,
    UserDevicesView,
    StateDevicesView,
)
from main.api.auth_views import AuthViewSet

router = DefaultRouter()

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),

    path('login/', AuthViewSet.as_view({'get': 'login', 'post':'login'}), name='login'),
    path('register/', AuthViewSet.as_view({'get': 'register', 'post': 'register'}), name='register'),
    path('logout/', AuthViewSet.as_view({'get': 'logout'}), name='logout'),
    path('delete/', AuthViewSet.as_view({'post': 'delete'}), name='delete'),

    path('dashboard/', DashboardView.as_view({'get': 'list'}), name='dashboard'),
    path('dashboard/floors/<int:floor_id>/', FloorDevicesView.as_view({'get': 'list'}), name='floor-rooms'),
    path('dashboard/floors/<int:floor_id>/room/<int:room_id>/', FloorDevicesView.as_view({'get': 'retrieve'}), name='room-devices'),
    path('dashboard/floors/<int:floor_id>/rooms.json', FloorRoomsAPIView.as_view({'get': 'list'}), name='floor-rooms-json'),
    path('dashboard/users/<int:user_id>/', UserDevicesView.as_view({'get': 'list'}), name='user-devices'),
    path('dashboard/state/<str:state>/', StateDevicesView.as_view({'get': 'list'}), name='state-devices'),

    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
