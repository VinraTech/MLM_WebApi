import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("This password must contain at least 1 uppercase letter."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter."
        )

class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("This password must contain at least 1 lowercase letter."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter."
        )

class SpecialCharacterValidator(object):
    def validate(self, password, user=None):
        special = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        if not sum(p in special for p in password) > 0:
            raise ValidationError(
                _("This password must contain at least 1 special character."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 special character."
        )

class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall("\d+", password):
            raise ValidationError(
                _("This password must contain at least 1 numerical letter."),
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 numerical letter."
        )

from .models import Customer

def GenerateCustomerID():
    last_id = Customer.objects.all().order_by('-id').first()
    if last_id and last_id.customer_id:
        c_id = last_id.customer_id
        new_id = int(c_id[5:]) + 1
        return c_id[:5]+str(new_id)
    else:
        return "N360680001"