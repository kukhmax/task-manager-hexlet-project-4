"""Module for testing users app."""

from django.contrib.auth import get_user
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import User

OK_CODE = 200
REDIRECT_CODE = 302


class UserTestCase(TestCase):
    """Test case class for users app."""

    def setUp(self):
        """Set up method for testing."""
        simple_user = User.objects.create(
            username='test_user1',
        )
        simple_user.set_password('test_pass1')
        simple_user.save()
        protected_user = User.objects.create(
            username='test_user2',
            password='test_pass2',
        )
        protected_user.save()


    def test_home_page(self):
        """Test for checking main page."""

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(
            response, template_name='users/home_page.html'
        )

    def test_users_list(self):
        """Test for checking users page."""
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(
            response, template_name='users/users_list.html'
        )
        self.assertQuerysetEqual(
            response.context_data['object_list'],
            User.objects.all(),
            ordered=False,
        )

    def test_create_user(self):
        """Test for checking registration."""
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(
            response,
            template_name='users/create_user.html',
        )
        response = self.client.post(reverse('user_create'), data={
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test',
            'password1': 'test12345.',
            'password2': 'test12345.',
        },
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully registered',
        )
        self.assertEqual(response.status_code, REDIRECT_CODE)
        self.assertEqual('test', User.objects.get(pk=3).first_name)
        self.assertEqual('test', User.objects.get(pk=3).last_name)
        self.assertEqual('test', User.objects.get(pk=3).username)

    def test_custom_login_mixin(self):
        """Test for checking how custom login mixin works."""
        response = self.client.get(reverse('user_update', args='1'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You are not authorized! Please log in.',
        )

    def test_user_updates_himself(self):
        """Test for checking how user can update himself."""
        self.client.force_login(User.objects.get(pk=1))
        response = self.client.get(reverse('user_update', args='1'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='users/update_user.html')
        response = self.client.post(reverse('user_update', args='1'), data={
            'first_name': 'test_update',
            'last_name': 'test_update',
            'username': 'test_update',
            'password1': 'test12345.',
            'password2': 'test12345.',
        },
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully updated',
        )
        self.assertEqual(response.status_code, REDIRECT_CODE)
        self.assertEqual('test_update', User.objects.get(pk=1).first_name)
        self.assertEqual('test_update', User.objects.get(pk=1).last_name)
        self.assertEqual('test_update', User.objects.get(pk=1).username)

    def test_user_updates_another(self):
        """Test for checking that user can not change other users."""
        self.client.force_login(User.objects.get(pk=1))
        response = self.client.get(reverse('user_update', args='2'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You do not have permission to change another user.',
        )

    def test_login_user(self):
        """Test for checking login page."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='users/login.html')
        response = self.client.post(reverse('login'), data={
            'username': 'test_user1',
            'password': 'test_pass1',
        },
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You are logged in',
        )
        self.assertEqual(response.status_code, REDIRECT_CODE)
        current_user = get_user(self.client)
        self.assertEqual(
            current_user.pk, User.objects.get(username='test_user1').pk,
        )

    def test_logout_user(self):
        """Test for checking logout feature."""
        self.client.force_login(User.objects.get(pk=1))
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You are logged out',
        )
        current_user = get_user(self.client)
        self.assertFalse(current_user.is_authenticated)

    def test_user_deletes_himself(self):
        """Test for checking how user can delete himself."""
        self.client.force_login(User.objects.get(pk=1))
        response = self.client.get(reverse('user_delete', args='1'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='users/delete_user_confirm.html')
        response = self.client.post(reverse('user_delete', args='1'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully deleted',
        )
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1)

    def test_user_deletes_another(self):
        """Test for checking that user can not delete other users."""
        self.client.force_login(User.objects.get(pk=1))
        response = self.client.get(reverse('user_delete', args='2'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You do not have permission to change another user.',
        )


    def test_signIn_signOut(self, page, base_url='http://127.0.0.1:8000'):
        page.goto('/')

        assert page.query_selector('text="Вход"') is not None