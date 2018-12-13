import re
from django.core.exceptions import ValidationError


def phone_number_validation(phone_number):
    if phone_number:
        regex = re.compile(r"^\+?1?\d{9,15}$")
        assert regex.fullmatch(phone_number), ValidationError(message="Wrong phone number")