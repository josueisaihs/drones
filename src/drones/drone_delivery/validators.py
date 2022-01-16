import re, logging

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_medication_code(value):
    # Allowed only upper case letters, underscore and numbers
    allows_characters = [chr(i) for i in range(65, 91)] + list(map(str, range(0, 10))) + ["_",]
    if not all([_chr_ in allows_characters for _chr_ in value]):
        raise ValidationError(
            _('the code "%(value)s" contains characters not allowed, allowed only upper case letters, underscore and numbers.'),
            params={'value': value},
        )
    return value

def validate_medication_name(value):
    # Allowed only letters, numbers, ‘-‘, ‘_’
    if not re.match(r'^[A-Za-z0-9_-]*$', value):
        raise ValueError(
            _(f"The name {value} contains characters not allowed, allowed only letters, numbers, '-', '_'")
        )
    return value