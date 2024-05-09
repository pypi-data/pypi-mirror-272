from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Usergroup(models.Model):

    user = models.ForeignKey(
        "User", related_name="user_UserGroup", on_delete=models.CASCADE
    )

    group = models.ForeignKey(
        "Group", related_name="group_UserGroup", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "UserGroup"
