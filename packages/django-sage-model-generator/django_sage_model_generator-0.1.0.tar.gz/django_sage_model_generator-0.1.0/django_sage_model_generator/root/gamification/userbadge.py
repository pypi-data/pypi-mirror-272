from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Userbadge(models.Model):

    user = models.ForeignKey(
        "User", related_name="user_UserBadge", on_delete=models.CASCADE
    )

    badge = models.ForeignKey(
        "Badge", related_name="badge_UserBadge", on_delete=models.CASCADE
    )

    date_acquisition = models.DateTimeField(
        _("Date_acquisition"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "UserBadge"
