from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class User(models.Model):

    username = models.CharField(
        _("Username"),
        help_text=_("phone number validator"),
        db_comment=_("..."),
        max_length=255,
    )

    password = models.CharField(
        _("Password"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    email = models.TextField(_("Email"), help_text=_("..."), db_comment=_("..."))

    phone_number = models.CharField(
        _("Phone_number"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    first_name = models.CharField(
        _("First_name"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    last_name = models.CharField(
        _("Last_name"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    is_active = models.BooleanField(
        _("Is_active"), help_text=_("..."), db_comment=_("...")
    )

    is_staff = models.BooleanField(
        _("Is_staff"), help_text=_("..."), db_comment=_("...")
    )

    is_superuser = models.BooleanField(
        _("Is_superuser"), help_text=_("..."), db_comment=_("...")
    )

    secret_key = models.CharField(
        _("Secret_key"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    last_login = models.DateTimeField(
        _("Last_login"), help_text=_("..."), db_comment=_("...")
    )

    date_joined = models.DateTimeField(
        _("Date_joined"), help_text=_("..."), db_comment=_("...")
    )

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "User"
