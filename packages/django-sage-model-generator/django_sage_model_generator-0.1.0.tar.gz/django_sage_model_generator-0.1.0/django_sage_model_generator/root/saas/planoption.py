from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Planoption(models.Model):

    title = models.CharField(
        _("Title"),
        null=False,
        unique=True,
        help_text=_("The name we have selected for this `option`."),
        db_comment=_("..."),
        max_length=255,
    )

    description = models.TextField(
        _("Description"),
        help_text=_("The extra description of this option."),
        db_comment=_("..."),
    )

    is_active = models.BooleanField(
        _("Is_active"),
        null=False,
        help_text=_("Show the `option` availability on website."),
        db_comment=_("..."),
        default=True,
    )

    priority = models.IntegerField(
        _("Priority"),
        null=False,
        help_text=_("order of display each option in website"),
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
        db_table = "PlanOption"

        indexes = [
            models.Index(fields=["title"], name="title_idx"),
        ]
