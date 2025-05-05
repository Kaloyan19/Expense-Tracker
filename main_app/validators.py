from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateRating:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if not 0.00 <= value <= 10.0:
            raise ValidationError(self.message)

@deconstructible
class ValidateReleaseYear:
    def __init__(self, message):
        self.message = message

    def __call__(self, value):
        if not 1990 <= value <= 2023:
            raise ValidationError(self.message)