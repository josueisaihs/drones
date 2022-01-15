
from django.views.generic import DetailView

from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView
)
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Drone, 
    Medication, 
    DeliveryPackage
)
from .serializers import (
    DroneSerializer, 
    MedicationSerializer,
    DeliveryPackageSerializer
)
from .filters import (
    DroneFilter, 
    MedicationFilter
)
from . import serializers

class DroneDetailView(DetailView):
    # Only for debug
    model = Drone

class DroneDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = DroneSerializer
    queryset = Drone.objects.all()
    lookup_field = "slug"

class DronesListCreateApiView(ListCreateAPIView):
    serializer_class = DroneSerializer
    queryset = Drone.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DroneFilter

class MedicationDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    lookup_field = "slug"

class MedicationsListCreateApiView(ListCreateAPIView):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MedicationFilter

class DeliveryPackageDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryPackageSerializer
    queryset = DeliveryPackage.objects.all()
    lookup_field = "slug"

class DeliveryPackageListCreateApiView(ListCreateAPIView):
    serializer_class = DeliveryPackageSerializer
    queryset = DeliveryPackage.objects.canLoad()

    def perform_create(self, serializer):
        print(serializer)
        instance = serializer.save()
