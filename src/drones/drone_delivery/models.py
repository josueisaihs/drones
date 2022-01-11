from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

from . import queryset

class Drone(models.Model):
    MODELS = (
        ("Lightweight", "Lightweight"),
        ("Middleweight", "Middleweight"), 
        ("Cruiserweight", "Cruiserweight"),
        ("Heavyweight", "Heavyweight")
    )

    STATES = (
        ("IDLE", "IDLE"),
        ("LOADING", "LOADING"),
        ("LOADED", "LOADED"),
        ("DELIVERING", "DELIVERING"),
        ("DELIVERED", "DELIVERED"),
        ("RETURNING", "RETURNING")
    )

    slug = models.SlugField(_("Slug"), max_length=150, blank=True, null=True)
    serial_number = models.DecimalField(_("Serial Number"), max_digits=100, decimal_places=0, unique=True)
    model = models.CharField(_("Model"), max_length=13, choices=MODELS)
    weight_limit = models.DecimalField(_("Weight Limit"), max_digits=5, decimal_places=2)
    battery_capacity = models.PositiveSmallIntegerField(_("Battery Capacity"))
    state = models.CharField(_("State"), max_length=10, choices=STATES)

    objects = queryset.DroneQuerySet.as_manager()    

    class Meta:
        verbose_name = _("Drone")
        verbose_name_plural = _("Drones")

    def __str__(self):
        return self.serial_number

    def get_absolute_url(self):
        return reverse("drone_delivery:drone-detail", kwargs={"slug": self.slug})

    def _get_unique_slug(self):
        slug = slugify(f'{self.serial_number}')
        unique_slug = slug
        num = 1
        while Drone.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)