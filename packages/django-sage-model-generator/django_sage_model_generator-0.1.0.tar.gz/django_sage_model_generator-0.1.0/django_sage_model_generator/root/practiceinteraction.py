from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Practiceinteraction(models.Model):

    participate = models.ForeignKey(
        "Bundleparticipation",
        related_name="participate_PracticeInteraction",
        on_delete=models.CASCADE,
    )

    lesson = models.ForeignKey(
        "Product", related_name="lesson_PracticeInteraction", on_delete=models.CASCADE
    )

    chapter = models.ForeignKey(
        "Product", related_name="chapter_PracticeInteraction", on_delete=models.CASCADE
    )

    gain_xp = models.IntegerField(
        _("Gain_xp"), null=False, help_text=_("..."), db_comment=_("..."), default=0
    )

    is_passed = models.BooleanField(
        _("Is_passed"),
        null=False,
        help_text=_("..."),
        db_comment=_("..."),
        default=False,
    )

    is_user_answered_correct = models.BooleanField(
        _("Is_user_answered_correct"),
        null=False,
        help_text=_("..."),
        db_comment=_("..."),
        default=False,
    )

    created = models.DateTimeField(
        _("Created"),
        null=False,
        help_text=_("Generate DateTime when new record inserted."),
        db_comment=_("..."),
        auto_now=True,
    )

    modified = models.DateTimeField(
        _("Modified"),
        null=False,
        help_text=_("Generate DateTime When existing record updated."),
        db_comment=_("..."),
        auto_now=True,
    )

    class Meta:
        db_table = "PracticeInteraction"
