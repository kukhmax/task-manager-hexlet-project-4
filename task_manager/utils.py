from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin for required login"""
    
    login_url = 'login'