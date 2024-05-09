from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Useraddress(models.Model):

    user = models.OneToOneField(
        "User", related_name="user_UserAddress", on_delete=models.CASCADE
    )

    province = models.CharField(
        _("Province"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    city = models.CharField(
        _("City"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    postal_address = models.CharField(
        _("Postal_address"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    postal_code = models.CharField(
        _("Postal_code"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    class Meta:
        db_table = "UserAddress"
