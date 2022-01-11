
from django.views.generic import DetailView
from django_filters.filterset import filterset_factory

from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.filters import (OrderingFilter)
from django_filters.rest_framework import (DjangoFilterBackend)

from . import queryset

from .models import (Drone)
from .serializers import (DroneSerializer)
from .filters import (DroneFilter)

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