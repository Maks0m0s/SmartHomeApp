from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main.api.home_views import HomeViewSet

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)