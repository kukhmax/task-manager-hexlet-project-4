from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, logout
from django.contrib import messages

from .models import User
from .forms import *



class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'

    
# def get_users(request):
#     users = User.objects.all()
#     context = {
#         'objects_list': users,
#     }
#     return render(request, 'users/index.html', context=context)


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users')
    success_message = 'User successfully registered'

    # def dispatch(self, request, *args, **kwargs):
    #     """Redirect unauthenticated users using error message.
    #     Returns:
    #         Redirect if user is not authenticated.
    #     """
    #     if not request.user.is_authenticated:
    #         messages.error(self.request, self.denied_without_login_message)
    #         return redirect('login')
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('login')
    
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = 'User successfully updated'

    # unable_to_change_others_message = 'You do not have permission to change another user.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('login')



class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('index')
    success_message = 'User successfully deleted'
    

class LoginUserView(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_success_url(self):
        return reverse_lazy('index')

def logout_user(request):
    logout(request)
    return redirect('login')