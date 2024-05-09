from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Certificate(models.Model):

    title = models.CharField(
        _("Title"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    slug = models.SlugField(_("Slug"), help_text=_("..."), db_comment=_("..."))

    picture = models.ImageField(
        _("Picture"), help_text=_("..."), db_comment=_("..."), uplod_to="uploads/"
    )

    alternate_text = models.CharField(
        _("Alternate_text"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    width_field = models.IntegerField(
        _("Width_field"), help_text=_("..."), db_comment=_("...")
    )

    height_field = models.IntegerField(
        _("Height_field"), help_text=_("..."), db_comment=_("...")
    )

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "Certificate"
