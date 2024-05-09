from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Notification(models.Model):

    summary = models.CharField(
        _("Summary"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    kind = models.CharField(choices=["general", "individual"], max_length=100)

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "Notification"
