from django.utils.translation import gettext as _
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import User
from .forms import CreateUserForm
from task_manager.utils import CustomLoginRequiredMixin, CustomDeleteView


class HomePageView(TemplateView):
    """View of home page"""

    template_name = "users/home_page.html"


class UserListView(ListView):
    """View of user's list"""

    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """View for create user."""

    model = User
    success_url = reverse_lazy('login')
    template_name = 'users/create_user.html'
    form_class = CreateUserForm
    success_message = _('User successfully registered')


class UserUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """View for update user."""

    model = User
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users')
    form_class = CreateUserForm
    success_message = _('User successfully updated')
    unable_to_change_others_message = _(
        'You do not have permission to change another user.',
    )

    def get(self, request, *args, **kwargs):
        """GET requests method.
        Returns:
            Execute GET request or redirect if user tries to change other users.
        """
        if request.user != self.get_object():
            messages.error(
                self.request, self.unable_to_change_others_message,
            )
            return redirect('users')
        return super().get(request, *args, **kwargs)


class UserDeleteView(CustomDeleteView):
    """View for user deletion page."""

    model = User
    template_name = 'users/delete_user_confirm.html'
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted')
    unable_to_change_others_message = _(
        'You do not have permission to change another user.',
    )
    deletion_error_message = _(
        'Cannot delete user because it is in use',
    )

    def get(self, request, *args, **kwargs):
        """GET requests method.
        Returns:
            Execute GET request or redirect
            if user tries to change other users.
        """
        if request.user != self.get_object():
            messages.error(
                self.request, self.unable_to_change_others_message,
            )
            return redirect('users')
        return super().get(request, *args, **kwargs)

class LoginUserView(SuccessMessageMixin, LoginView):
    """View for login page."""

    template_name = 'users/login.html'
    next_page = reverse_lazy('home')
    success_message = _('You are logged in')


class LogoutUserView(LogoutView):
    """View for logout page."""

    next_page = reverse_lazy('home')
    logout_message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method but with message for user."""
        messages.info(
            self.request, self.logout_message,
        )
        return super().dispatch(request, *args, **kwargs)
