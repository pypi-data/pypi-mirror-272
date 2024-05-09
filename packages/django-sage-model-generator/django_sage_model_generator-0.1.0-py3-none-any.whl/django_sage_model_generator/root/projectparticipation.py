from django.db import models
from django.utils.translation import gettext_lazy as _


from helpers.choices import Status

from helpers.choices import ScopeStatus

from helpers.choices import QuestionTypes

from helpers.choices import PaymentMethod

from helpers.choices import Levels

from helpers.choices import SubscriptionStatusChoices

from helpers.choices import DiscountTypes


class Projectparticipation(models.Model):

    bundle = models.ForeignKey(
        "Product", related_name="bundle_ProjectParticipation", on_delete=models.CASCADE
    )

    project = models.ForeignKey(
        "Product", related_name="project_ProjectParticipation", on_delete=models.CASCADE
    )

    agreement = models.BooleanField(
        _("Agreement"),
        null=False,
        help_text=_("..."),
        db_comment=_("..."),
        default=True,
    )

    user = models.ForeignKey(
        "User", related_name="user_ProjectParticipation", on_delete=models.CASCADE
    )

    is_finished = models.BooleanField(
        _("Is_finished"),
        null=False,
        help_text=_(
            "This field becomes True when all the content of the \nbundle is completed and 100% of the duration has been \ncompleted and at least one project has been completed."
        ),
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
        db_table = "ProjectParticipation"
