from django.db import models
from django.utils.translation import gettext_lazy as _

MAX_LENGTH = 100

class Label(models.Model):
    """"Model of task's label"""
    name = models.CharField(
        max_length=MAX_LENGTH, unique=True, verbose_name=_('Name'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date of create'),
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = _("Labels")
