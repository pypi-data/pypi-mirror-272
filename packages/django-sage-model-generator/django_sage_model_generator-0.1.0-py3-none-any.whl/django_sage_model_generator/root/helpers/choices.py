from django.db import models
from django.utils.translation import gettext as _


class Status(models.TextChoices):

    GENERAL = ('general', _('general'))

    INDIVIDUAL = ('individual', _('individual'))


class ScopeStatus(models.TextChoices):

    DIVISION = ('division', _('division'))

    BUNDLE = ('bundle', _('bundle'))

    COURSE = ('course', _('course'))

    LESSON = ('lesson', _('lesson'))

    CHAPTER = ('chapter', _('chapter'))

    PROJECT_ = ('project_', _('project_'))

    PRACTICE = ('practice', _('practice'))


class QuestionTypes(models.TextChoices):

    CHECKBOX = ('checkbox', _('checkbox'))

    RADIO = ('radio', _('radio'))

    PLACEHOLDER = ('placeholder', _('placeholder'))

    CONDITIONAL = ('conditional', _('conditional'))

    CODE = ('code', _('code'))


class PaymentMethod(models.TextChoices):

    FREEMIUM = ('freemium', _('freemium'))

    PREMIUM = ('premium', _('premium'))

    ESHOP = ('eshop', _('eshop'))


class Levels(models.TextChoices):

    BEGINNER = ('beginner', _('beginner'))

    INTERMEDIATE = ('intermediate', _('intermediate'))

    ADVANCE = ('advance', _('advance'))

    PRODUCTIVE = ('productive', _('productive'))


class SubscriptionStatusChoices(models.TextChoices):

    PENDING = ('pending', _('pending'))

    SUBSCRIBED = ('subscribed', _('subscribed'))

    UNSUBSCRIBED = ('unsubscribed', _('unsubscribed'))


class DiscountTypes(models.TextChoices):

    PERCENTAGE_DISCOUNT = ('percentage_discount', _('percentage_discount'))

    FIXED_DISCOUNT = ('fixed_discount', _('fixed_discount'))

