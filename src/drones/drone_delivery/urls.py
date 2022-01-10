from django.urls import path

from .views import (DroneDetailView)

urlpatterns = [
    path("drone/<slug:slug>/detail/", DroneDetailView.as_view(), name="drone-detail"),
]