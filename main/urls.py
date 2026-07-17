from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from main.api.home_views import HomeViewSet
from main.api.dashboard_views import (
    DashboardView,
    FloorDetailView,
    RoomDetailView,
    UserDetailView,
    StateDetailView,
)
from main.api.auth_views import AuthViewSet

router = DefaultRouter()

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),

    path('login/', AuthViewSet.as_view({'get': 'login', 'post': 'login'}), name='login'),
    path('register/', AuthViewSet.as_view({'get': 'register', 'post': 'register'}), name='register'),
    path('logout/', AuthViewSet.as_view({'get': 'logout'}), name='logout'),
    path('delete/', AuthViewSet.as_view({'post': 'delete'}), name='delete'),

    path('dashboard/', DashboardView.as_view({'get': 'list'}), name='dashboard'),

    path('dashboard/floors/', FloorDetailView.as_view({'get': 'list'}), name='floors-list'),
    path('dashboard/floor/<int:floor_id>/', FloorDetailView.as_view({'get': 'retrieve'}), name='floor-detail'),
    path('dashboard/floor/<int:floor_id>/room/<int:room_id>/', RoomDetailView.as_view({'get': 'retrieve'}), name='room-detail'),

    path('dashboard/persons/', UserDetailView.as_view({'get': 'list'}), name='persons-list'),
    path('dashboard/user/<int:user_id>/', UserDetailView.as_view({'get': 'retrieve'}), name='user-detail'),

    path('dashboard/states/', StateDetailView.as_view({'get': 'list'}), name='states-list'),
    path('dashboard/state/<str:state>/', StateDetailView.as_view({'get': 'retrieve'}), name='state-detail'),

    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
