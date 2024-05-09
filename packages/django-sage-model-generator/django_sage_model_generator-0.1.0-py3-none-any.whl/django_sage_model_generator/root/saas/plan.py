from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Plan(models.Model):

    title = models.CharField(
        _("Title"),
        null=False,
        unique=True,
        help_text=_("The name we have selected for this `plan`."),
        db_comment=_("..."),
        max_length=100,
    )

    price = models.FloatField(
        _("Price"),
        null=False,
        help_text=_("The current `price` for this `plan`."),
        db_comment=_("..."),
    )

    is_active = models.BooleanField(
        _("Is_active"),
        null=False,
        help_text=_("Show the `plan` availability on website."),
        db_comment=_("..."),
        default=True,
    )

    created = models.DateTimeField(
        _("Created"),
        null=False,
        help_text=_("Generate DateTime when new record inserted."),
        db_comment=_("..."),
        auto_now=True,
    )

    modified = models.DateTimeField(
        _("Modified"),
        null=False,
        help_text=_("Generate DateTime When existing record updated."),
        db_comment=_("..."),
        auto_now=True,
    )

    class Meta:
        db_table = "Plan"

        indexes = [
            models.Index(fields=["title"], name="title_idx"),
        ]
