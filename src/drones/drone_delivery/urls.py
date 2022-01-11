from django.urls import path

from .views import (DroneDetailView, DronesListCreateApiView, DroneDetailApiView, MedicationDetailApiView, MedicationsListCreateApiView)

urlpatterns = [
    path("drone/<slug:slug>/detail/", DroneDetailView.as_view(), name="drone-detail"),

    # API
    path("api/drone/list/", DronesListCreateApiView.as_view(), name="api-drone-list"),
    path("api/drone/<slug:slug>/detail/", DroneDetailApiView.as_view(), name="api-drone-detail"),
    path("api/medication/list/", MedicationsListCreateApiView.as_view(), name="api-medication-list"),
    path("api/medication/<slug:slug>/detail/", MedicationDetailApiView.as_view(), name="api-medication-detail")
]