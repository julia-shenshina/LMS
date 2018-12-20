from lms.models.validators import *


def test_phone_validator():
    phone_numbers = [
        '+79999999999',
        '89999999999',
        '79518213990',
        '+7 (919) 999 99 99',
        '8(918)9779797',
        '8-999-999-99-99'
    ]
    for phone_number in phone_numbers:
        phone_number_validation(phone_number)

