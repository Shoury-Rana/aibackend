# endpoint/urls.py
from django.urls import path
from .views import endpointAPIView

urlpatterns = [
    path('endpoint/', endpointAPIView.as_view(), name='endpoint-api'),
]