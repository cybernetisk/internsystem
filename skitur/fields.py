from django.core.exceptions import ValidationError
from django.db import models

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


class PhoneField(models.Field):

    description = 'Phone number field!'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        super(PhoneField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if value == None:
            return None
        try:
            num = phonenumbers.parse(value, 'NO')
            return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            raise ValidationError('Please enter a valid phone number.')

    def get_prep_value(self, value):
        if value == None:
            return None
        try:
            num = phonenumbers.parse(value, 'NO')
            return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            raise ValidationError('Please enter a valid phone number.')

    def value_from_object(self, obj):
        num = phonenumbers.parse(getattr(obj, self.attname), None)
        return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
