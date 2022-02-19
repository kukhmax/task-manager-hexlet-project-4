"""Module with filters for tasks app."""

from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from labels.models import Label
from tasks.models import Task


class TaskFilter(FilterSet):
    """Custom filter for tasks page."""

    own_tasks = BooleanFilter(
        field_name='author',
        label=_('Show_own_tasks'),
        method='filter_own_tasks',
        widget=CheckboxInput,
    )

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
    )

    def filter_own_tasks(self, queryset, name, value):
        """Show tasks where author is current user if needed.
        Returns:
            Queryset with tasks: filtered by current user or not.
        """
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta (object):
        """Meta information of filter."""

        model = Task
        fields = [
            'status',
            'executor',
            'labels',
            'own_tasks',
        ]
