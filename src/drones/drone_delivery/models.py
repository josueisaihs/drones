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


class Medication(models.Model):
    slug = models.SlugField(_("Slug"), max_length=350, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=150)
    weight = models.DecimalField(_("Weight"), max_digits=5, decimal_places=2)
    code = models.CharField(_("Code"), max_length=150)
    height = models.PositiveIntegerField(
        default=0, editable=False, null=True, blank=True
    )
    width = models.PositiveIntegerField(
        default=0, editable=False, null=True, blank=True
    )
    image = models.ImageField(_("Image"), upload_to="medications/%Y/%m/%d/", height_field="height", width_field="width", max_length=None)

    def _get_unique_slug(self):
        slug = slugify(f'{self.name} {self.code}')
        unique_slug = slug
        num = 1
        while Medication.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)