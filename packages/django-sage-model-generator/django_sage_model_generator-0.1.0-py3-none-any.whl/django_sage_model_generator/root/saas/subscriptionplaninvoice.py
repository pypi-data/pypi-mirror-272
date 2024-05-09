from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Subscriptionplaninvoice(models.Model):

    subscription = models.ForeignKey(
        "Subscription",
        related_name="subscription_SubscriptionPlanInvoice",
        on_delete=models.CASCADE,
    )

    bank_portal = models.ForeignKey(
        "Bankportal",
        related_name="bank_portal_SubscriptionPlanInvoice",
        on_delete=models.CASCADE,
    )

    period_start_date = models.DateTimeField(
        _("Period_start_date"),
        null=False,
        help_text=_("The start time interval covered by this invoice"),
        db_comment=_("..."),
    )

    period_end_date = models.DateTimeField(
        _("Period_end_date"),
        help_text=_("The end time interval covered by this invoice"),
        db_comment=_("..."),
    )

    description = models.TextField(
        _("Description"),
        help_text=_("A short textual description of the invoice."),
        db_comment=_("..."),
    )

    amount = models.FloatField(
        _("Amount"),
        help_text=_("The amount of payment due for this invoice."),
        db_comment=_("..."),
    )

    paid_at = models.DateTimeField(
        _("Paid_at"),
        help_text=_("The timestamp when this invoice was paid."),
        db_comment=_("..."),
    )

    is_paid = models.BooleanField(
        _("Is_paid"),
        null=False,
        help_text=_(
            "Whenever we don&#39;t have end_date that means this invoice does not paid by user."
        ),
        db_comment=_("..."),
        default=False,
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
        db_table = "SubscriptionPlanInvoice"
