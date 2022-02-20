from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Mixin with added login required message."""

    denied_without_login_message = _('You are not authorized! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        """Redirect unauthenticated users using error message.
        Returns:
            Redirect if user is not authenticated.
        """
        if not request.user.is_authenticated:
            messages.error(self.request, self.denied_without_login_message)
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class CustomDeleteView(
    SuccessMessageMixin,
    CustomLoginRequiredMixin,
    DeleteView,
):
    """Custom view for deletion pages."""

    deletion_error_message = None
    success_url = None

    def post(self, request, *args, **kwargs):
        """POST requests method.
        Returns:
            Execute POST request or redirect
            if user tries to delete object in use.
        """
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request, self.deletion_error_message,
            )
            return redirect(self.success_url)
