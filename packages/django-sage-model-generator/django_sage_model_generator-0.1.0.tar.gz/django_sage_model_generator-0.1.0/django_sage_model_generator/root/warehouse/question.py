from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Question(models.Model):

    product = models.ForeignKey(
        "Product", related_name="product_Question", on_delete=models.CASCADE
    )

    text_ = models.CharField(
        _("Text_"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    kind = models.CharField(
        choices=["checkbox", "radio", "placeholder", "conditional", "code"],
        max_length=100,
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
        db_table = "Question"
