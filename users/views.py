from django.utils.translation import gettext as _
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login as auth_login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .models import User
from .forms import  UserRegisterForm, LoginUserForm


class HomePageView(TemplateView):
    """View of home page"""

    template_name = "users/home_page.html"

class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/create_user.html'
    success_url = reverse_lazy('users')
    success_message = 'User successfully registered'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('users')

class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users')
    success_message = 'User successfully updated'

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



class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/delete_user_confirm.html'
    success_url = reverse_lazy('index')
    success_message = 'User successfully deleted'

    unable_to_change_others_message = _(
        'You do not have permission to change another user.',
    )
    deletion_error_message = _(
        'Cannot delete user because it is in use',
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
    

class LoginUserView(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        return reverse_lazy('index')

# def logout_user(request):
#     logout(request)
#     return redirect('login')

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


