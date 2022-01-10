from django.shortcuts import render
from django.views.generic import DetailView

from . import models

class DroneDetailView(DetailView):
    model = models.Drone
