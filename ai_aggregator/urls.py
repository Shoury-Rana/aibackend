# ai_aggregator/urls.py
from django.contrib import admin
from django.urls import path, include # Add include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('endpoint.urls')), # Include endpoint app urls under /api/
]