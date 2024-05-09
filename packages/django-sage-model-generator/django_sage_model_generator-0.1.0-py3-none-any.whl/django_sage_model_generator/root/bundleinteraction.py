from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Bundleinteraction(models.Model):

    participate = models.ForeignKey(
        "Bundleparticipation",
        related_name="participate_BundleInteraction",
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        "Product", related_name="course_BundleInteraction", on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(
        "Product", related_name="lesson_BundleInteraction", on_delete=models.CASCADE
    )

    chapter = models.ForeignKey(
        "Product", related_name="chapter_BundleInteraction", on_delete=models.CASCADE
    )

    gain_xp = models.IntegerField(
        _("Gain_xp"), null=False, help_text=_("..."), db_comment=_("..."), default=0
    )

    lose_xp = models.IntegerField(
        _("Lose_xp"), null=False, help_text=_("..."), db_comment=_("..."), default=0
    )

    mistaken_times = models.IntegerField(
        _("Mistaken_times"),
        null=False,
        help_text=_("..."),
        db_comment=_("..."),
        default=0,
    )

    got_help = models.IntegerField(
        _("Got_help"), null=False, help_text=_("..."), db_comment=_("..."), default=0
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
        default=True,
    )

    user_answers = models.TextField(
        _("User_answers"), help_text=_("..."), db_comment=_("...")
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
        db_table = "BundleInteraction"
