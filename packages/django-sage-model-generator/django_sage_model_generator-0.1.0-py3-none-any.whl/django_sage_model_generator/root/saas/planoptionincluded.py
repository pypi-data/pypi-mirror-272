from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Planoptionincluded(models.Model):

    plan = models.ForeignKey(
        "Plan", related_name="plan_PlanOptionIncluded", on_delete=models.CASCADE
    )

    option = models.ForeignKey(
        "Planoption", related_name="option_PlanOptionIncluded", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "PlanOptionIncluded"
