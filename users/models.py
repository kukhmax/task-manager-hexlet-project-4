"""Models for users app."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A task manager user."""

    def __str__(self):
        """Present object as a string.
        Returns:
            Full name of the user.
        """
        return self.get_full_name()
