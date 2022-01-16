
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
    DeliveryPackage,
    Package
)
from .serializers import (
    DroneSerializer, 
    MedicationSerializer,
    DeliveryPackageSerializer,
    PackageSerializer
)
from .filters import (
    DroneFilter, 
    MedicationFilter,
    DeliveryPackageFilter
)

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

class PackageDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer
    queryset = DeliveryPackage.objects.all()
    lookup_field = "slug"
    
class PackageListCreateApiView(ListCreateAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

class DeliveryPackageDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryPackageSerializer
    queryset = DeliveryPackage.objects.all()
    lookup_field = "slug"

class DeliveryPackageListCreateApiView(ListCreateAPIView):
    serializer_class = DeliveryPackageSerializer
    queryset = DeliveryPackage.objects.canLoad()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DeliveryPackageFilter
    
    # todo: Change the drone's state, IDLE to LOADING
