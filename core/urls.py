from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from api.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls, name='api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
