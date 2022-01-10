from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


from .models import (Drone)

class DroneForm(ModelForm):
    class Meta:
        model = Drone
        fields = "__all__"

        error_messages = {
            'serial_number': {
                'max_length': _("This Serial Number is too long."),
            },
        }

    def clean_battery_capacity(self):
        data = self.cleaned_data["battery_capacity"]
        if 0 <= data <= 100:
            return data
        else:
            self.add_error("battery_capacity", _(f"The value {data} for the Battery Capacity is wrong. Battery Capacity must be value between 0 and 100"))

    def clean_weight_limit(self):
        data = self.cleaned_data["weight_limit"]

        if 0 < data <= 500:
            return data
        else:
            self.add_error("weight_limit", _(f"The value {data} as Weight Limit is wrong. The value must be a maximum of 500g."))