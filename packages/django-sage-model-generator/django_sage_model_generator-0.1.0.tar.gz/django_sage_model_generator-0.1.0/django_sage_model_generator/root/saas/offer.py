from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Offer(models.Model):

    title = models.CharField(
        _("Title"),
        null=False,
        unique=True,
        help_text=_("A UNIQUE name we selected for this offer."),
        db_comment=_("..."),
        max_length=200,
    )

    is_active = models.BooleanField(
        _("Is_active"),
        null=False,
        help_text=_("Show the `offer` availability on website."),
        db_comment=_("..."),
        default=True,
    )

    start_date = models.DateTimeField(
        _("Start_date"),
        null=False,
        help_text=_("The start time period during which this offer is available."),
        db_comment=_("..."),
    )

    end_date = models.DateTimeField(
        _("End_date"),
        null=False,
        help_text=_("The end time period during which this offer is available."),
        db_comment=_("..."),
    )

    description = models.TextField(
        _("Description"),
        help_text=_("A detailed textual description of the offer."),
        db_comment=_("..."),
    )

    discount_type = models.CharField(
        choices=["percentage_discount", "fixed_discount"], max_length=100
    )

    discount_amount = models.DecimalField(
        _("Discount_amount"),
        help_text=_("a fixed amount-based discount"),
        db_comment=_("..."),
    )

    discount_percentage = models.DecimalField(
        _("Discount_percentage"),
        help_text=_("a percentage discount"),
        db_comment=_("..."),
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
        db_table = "Offer"

        indexes = [
            models.Index(fields=["title"], name="title_idx"),
        ]
