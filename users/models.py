"""Models for users app."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A task manager user."""

    def __str__(self):
        return self.get_full_name()
