from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Userprofile(models.Model):

    notifications = models.IntegerField(
        _("Notifications"), help_text=_("..."), db_comment=_("...")
    )

    certifications = models.IntegerField(
        _("Certifications"), help_text=_("..."), db_comment=_("...")
    )

    tags = models.IntegerField(_("Tags"), help_text=_("..."), db_comment=_("..."))

    favorites = models.IntegerField(
        _("Favorites"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "UserProfile"
