# файл urls.py в главной папке проекта

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tpi_drf.urls')),
]
