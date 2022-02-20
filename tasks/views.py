from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django_filters.views import FilterView 


from .models import Task
from task_manager.utils import CustomLoginRequiredMixin
from .filters import TaskFilter

class TaskListView(CustomLoginRequiredMixin, FilterView):
    """View of page with tasks and filter of tasks"""

    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

class TaskCreateView(
    SuccessMessageMixin, CustomLoginRequiredMixin, CreateView
):
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
    template_name = 'tasks/task_details.html'

class TaskUpdateView(
    SuccessMessageMixin, CustomLoginRequiredMixin, UpdateView,
):
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
    """View for task deletion page."""

    model = Task
    template_name = 'tasks/task_delete_confirm.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    unable_to_delete_others_tasks = _(
        'Task can only be deleted by its author',
    )

    def get(self, request, *args, **kwargs):
        """GET requests method.
        Returns:
            Execute GET request or redirect if user tries to delete not his own task.
        """
        if request.user != self.get_object().author:
            messages.error(
                self.request, self.unable_to_delete_others_tasks,
            )
            return redirect('tasks')
        return super().get(request, *args, **kwargs)