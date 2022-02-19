"""Module with views logic of the labels app."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Label
from task_manager.utils import CustomLoginRequiredMixin


class LabelListView(ListView):
    """View of labels"""
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'


class LabelCreateView(SuccessMessageMixin, CreateView):
    """View for create label page."""

    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('label successfully created')
    template_name = 'labels/label_create.html'
    fields = ['name']

class LabelUpdateView(
    SuccessMessageMixin, CustomLoginRequiredMixin, UpdateView,
):
    """View for update label page."""

    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('label successfully updated')
    template_name = 'labels/label_update.html'
    fields = ['name']

class LabelDeleteView(
    SuccessMessageMixin, CustomLoginRequiredMixin, DeleteView,
):
    """View for label deletion page."""

    model = Label
    template_name = 'labels/label_delete_confirm.html'
    success_url = reverse_lazy('labels')
    success_message = _('label successfully deleted')
    deletion_error_message = _(
        'Can not delete label because it is in use',
    )
