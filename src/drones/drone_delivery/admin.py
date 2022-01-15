from django.contrib import admin
from django.utils.html import format_html

from .models import (
    DeliveryPackage,
    Drone,
    Medication
)

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    '''Admin View for Drone'''
    list_display = ('slug', 'serial_number', 'model', 'state', 'weight_limit', 'battery_capacity')
    list_filter = ('model', 'state')
    readonly_fields = ('slug',)
    search_fields = ('slug', 'serial_number', 'model', 'weight_limit', 'battery_capacity')
    ordering = ('serial_number', 'model')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    '''Admin View for Medication'''

    list_display = ('slug', 'name', 'weight', 'code', 'thumbnail')
    readonly_fields = ('slug',)
    search_fields = ('slug', 'name', 'weight', 'code')
    ordering = ('name', 'weight')

    def thumbnail(self, obj):
        return format_html(f"<div class='photo-thumbnail'><img src='{obj.image.url}'></div>")

@admin.register(DeliveryPackage)
class DeliveryPackageAdmin(admin.ModelAdmin):
    '''Admin View for DeliveryPackage'''
    list_display = ('slug', 'drone',)
    list_filter = ('drone__model',)
    readonly_fields = ('slug',)
    search_fields = ('slug', 'drone__serial_number', 'drone__model', 'drone__weight_limit', 'drone__battery_capacity')
    ordering = ('drone__serial_number',)
