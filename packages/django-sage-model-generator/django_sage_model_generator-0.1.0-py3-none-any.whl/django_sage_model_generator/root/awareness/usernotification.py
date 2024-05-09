from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Usernotification(models.Model):

    user = models.ForeignKey(
        "User", related_name="user_UserNotification", on_delete=models.CASCADE
    )

    notification = models.ForeignKey(
        "Notification",
        related_name="notification_UserNotification",
        on_delete=models.CASCADE,
    )

    is_active = models.BooleanField(
        _("Is_active"), help_text=_("..."), db_comment=_("..."), default=True
    )

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "UserNotification"
