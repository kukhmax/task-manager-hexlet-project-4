from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)


from .models import Task
from task_manager.utils import CustomLoginRequiredMixin

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

class TaskCreateView(SuccessMessageMixin, CustomLoginRequiredMixin, CreateView):
    """View for create task page."""

    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')
    template_name = 'tasks/task_create.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']

    def form_valid(self, form):
        """Set author of task as active user."""
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskDetailView(DetailView):
    """View details of task"""

    model = Task
    template_name = 'tasks/task_detail.html'

class TaskUpdateView(SuccessMessageMixin, CustomLoginRequiredMixin, UpdateView):
    """View for update task page."""

    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')
    template_name = 'tasks/task_update.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']

    def form_valid(self, form):
        """Set author of task as active user."""
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskDeleteView(SuccessMessageMixin, CustomLoginRequiredMixin, DeleteView):
    """View for delete task page."""

    model = Task
    template_name = 'tasks/task_delete_confirm.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    deletion_error_message = _(
        'Can not delete task because it is in use',
    )


