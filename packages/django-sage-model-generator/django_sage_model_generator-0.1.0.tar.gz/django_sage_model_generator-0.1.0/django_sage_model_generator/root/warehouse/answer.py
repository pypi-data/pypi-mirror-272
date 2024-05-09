from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Answer(models.Model):

    question = models.ForeignKey(
        "Question", related_name="question_Answer", on_delete=models.CASCADE
    )

    text_ = models.CharField(
        _("Text_"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    is_correct = models.CharField(
        _("Is_correct"), help_text=_("..."), db_comment=_("..."), max_length=255
    )

    priorty = models.IntegerField(_("Priorty"), help_text=_("..."), db_comment=_("..."))

    order_placeholder = models.IntegerField(
        _("Order_placeholder"), help_text=_("..."), db_comment=_("...")
    )

    created = models.DateTimeField(
        _("Created"), help_text=_("..."), db_comment=_("...")
    )

    modified = models.DateTimeField(
        _("Modified"), help_text=_("..."), db_comment=_("...")
    )

    class Meta:
        db_table = "Answer"
