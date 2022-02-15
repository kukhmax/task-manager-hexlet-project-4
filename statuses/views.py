"""Module with views logic of the statuses app."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)


from .models import Status
from task_manager.utils import CustomLoginRequiredMixin

class StatusListView(ListView):
    """View of statuses"""
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

class StatusCreateView(SuccessMessageMixin, CreateView):
    """View for create status page."""

    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    template_name = 'statuses/status_create.html'
    fields = ['name']

class StatusUpdateView(SuccessMessageMixin, CustomLoginRequiredMixin, UpdateView):
    """View for update status page."""

    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')
    template_name = 'statuses/status_update.html'
    fields = ['name']

class StatusDeleteView(SuccessMessageMixin, CustomLoginRequiredMixin, DeleteView):
    """View for status deletion page."""

    model = Status
    template_name = 'statuses/status_delete_confirm.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    deletion_error_message = _(
        'Can not delete status because it is in use',
    )
