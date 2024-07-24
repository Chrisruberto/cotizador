from django.urls import path
from .views import YourAPIView

urlpatterns = [
    path('', YourAPIView.as_view(), name='endpoint-name'),
]