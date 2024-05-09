from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Product(models.Model):

    sku = models.CharField(
        _("Sku"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    title = models.CharField(
        _("Title"), null=False, help_text=_("..."), db_comment=_("..."), max_length=255
    )

    slug = models.SlugField(_("Slug"), help_text=_("..."), db_comment=_("..."))

    parent = models.ForeignKey(
        "Product", related_name="parent_Product", on_delete=models.CASCADE
    )

    scope = models.CharField(
        choices=[
            "division",
            "bundle",
            "course",
            "lesson",
            "chapter",
            "project_",
            "practice",
        ],
        max_length=100,
    )

    description = models.TextField(
        _("Description"), help_text=_("..."), db_comment=_("...")
    )

    is_buyable = models.TextField(
        _("Is_buyable"), help_text=_("..."), db_comment=_("..."), default=False
    )

    experience = models.IntegerField(
        _("Experience"), help_text=_("..."), db_comment=_("...")
    )

    difficulty = models.CharField(
        choices=["beginner", "intermediate", "advance", "productive"], max_length=100
    )

    priority = models.IntegerField(
        _("Priority"), help_text=_("..."), db_comment=_("...")
    )

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "Product"
