from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class PositiveNumberValidator:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if value <= 0:
            raise ValidationError(self.message)