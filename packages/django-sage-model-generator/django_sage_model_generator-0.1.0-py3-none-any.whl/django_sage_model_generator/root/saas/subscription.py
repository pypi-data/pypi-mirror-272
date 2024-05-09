from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Subscription(models.Model):

    user = models.ForeignKey(
        "User", related_name="user_Subscription", on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        "Plan", related_name="plan_Subscription", on_delete=models.CASCADE
    )

    offer = models.ForeignKey(
        "Offer", related_name="offer_Subscription", on_delete=models.CASCADE
    )

    is_current = models.BooleanField(
        _("Is_current"),
        null=False,
        help_text=_(
            "this subscription is currently active or not.\nThe past subscriptions will remain `is_current` to `False`"
        ),
        db_comment=_("..."),
        default=False,
    )

    status = models.CharField(
        choices=["pending", "subscribed", "unsubscribed"], max_length=100
    )

    trial_period_start_date = models.DateTimeField(
        _("Trial_period_start_date"),
        help_text=_(
            "The lower boundary of the trial\nperiod (if any) for this subscription."
        ),
        db_comment=_("..."),
    )

    trial_period_end_date = models.DateTimeField(
        _("Trial_period_end_date"),
        help_text=_(
            "The upper boundary of the trial period\n(if any) for this subscription."
        ),
        db_comment=_("..."),
    )

    subscribe_after_trial = models.BooleanField(
        _("Subscribe_after_trial"),
        help_text=_(
            "A flag denoting if the subscription will be \nautomatically renewed after the trial period \n(if any) ends."
        ),
        db_comment=_("..."),
        default=False,
    )

    date_subscribed = models.DateTimeField(
        _("Date_subscribed"),
        help_text=_("When the user subscribed to this subscription."),
        db_comment=_("..."),
    )

    date_unsubscribed = models.DateTimeField(
        _("Date_unsubscribed"),
        help_text=_(
            "The date when that user unsubscribed from this subscription. \ne.g. automatically unsubscribing a user from his/her service \nWhen the subscription due date is over."
        ),
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
        db_table = "Subscription"
