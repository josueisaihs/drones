from django.urls import path

from .views import (DroneDetailView, DronesListView)

urlpatterns = [
    path("drone/<slug:slug>/detail/", DroneDetailView.as_view(), name="drone-detail"),

    # API
    path("api/drone/list/", DronesListView.as_view(), name="api-drone-list")
]