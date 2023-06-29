from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    """
    Ensure `date_created` and `date_updated` timestamps are recorded for a Model instance,
    """

    class Meta:
        abstract = True

    date_created = models.DateTimeField(
        _('date_created'), auto_now_add=True,
        help_text=_('Timestamp for creation of this record'))

    date_updated = models.DateTimeField(
        _('date_updated'), auto_now=True,
        help_text=_('Timestamp for latest update of this record'))
