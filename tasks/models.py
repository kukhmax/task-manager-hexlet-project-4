from django.db import models
from django.utils.translation import gettext as _

from statuses.models import Status
from users.models import User

MAX_LENGTH = 100
MAX_LENGTH_OF_DESCRIPTION = 600

class Task(models.Model):
    """Model of task"""

    name = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name=_("Name"),
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        max_length=MAX_LENGTH_OF_DESCRIPTION,
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Auhtor'),
        related_name='tasks_author',
    )
    executor = models.ForeignKey(
        User,
        verbose_name=_('Executor'),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='tasks_executor',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of create'),
    )
    # labels = models.ManyToManyField(
    #     'labels.Label',
    #     verbose_name=_('Labels'),
    #     blank=True,
    #     related_name='tasks',
    #     through='TaskLabelRelation',
    #     through_fields=('task', 'label'),
    # )

    def __str__(self):
        return self.name
    
    class Meta:

        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']