from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Badge(models.Model):

    title = models.CharField(
        _("Title"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    slug = models.SlugField(_("Slug"), help_text=_("..."), db_comment=_("..."))

    scope = models.CharField(
        _("Scope"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    svg = models.ImageField(
        _("Svg"), help_text=_("..."), db_comment=_("..."), uplod_to="uploads/"
    )

    description = models.TextField(
        _("Description"), help_text=_("..."), db_comment=_("...")
    )

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "Badge"
