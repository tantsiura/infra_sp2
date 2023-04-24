from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Checking if the year is correct."""
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'Year value cannot be later than {now}'
        )
