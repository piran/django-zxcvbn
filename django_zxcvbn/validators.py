from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import zxcvbn

# Settings
PASSWORD_MIN_LENGTH = getattr(settings, "PASSWORD_MIN_LENGTH", 8)   # This is a sensible minimum
PASSWORD_MAX_LENGTH = getattr(settings, "PASSWORD_MAX_LENGTH", 128) # Django auth user model is max_length 128
PASSWORD_MIN_ENTROPY = getattr(settings, "ZXCVBN_MIN_ENTROPY", 25)


class LengthValidator(object):
    code = "length"

    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value):
        if self.min_length and len(value) < self.min_length:
            raise ValidationError(
                message=_("Must be %s characters or more") % self.min_length,
                code=self.code)
        elif self.max_length and len(value) > self.max_length:
            raise ValidationError(
                message=_("Must be %s characters or less") % self.max_length,
                code=self.code)


class ZXCVBNValidator(object):
    code = "zxcvbn"

    def __call__(self,value):
        res = zxcvbn.password_strength(value)
        if res.get('entropy') < PASSWORD_MIN_ENTROPY:
            raise ValidationError(
                _("Password is too weak"),
                code=self.code)


length_validator = LengthValidator(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
zxcvbn_validator = ZXCVBNValidator()
