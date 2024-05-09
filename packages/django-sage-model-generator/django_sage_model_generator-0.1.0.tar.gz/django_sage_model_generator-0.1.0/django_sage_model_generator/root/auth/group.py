from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Group(models.Model):

    name = models.CharField(
        _("Name"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    class Meta:
        db_table = "Group"
