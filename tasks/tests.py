"""Module for testing tasks app."""

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from users.models import User
from labels.models import Label
from statuses.models import Status
from .models import Task

OK_CODE = 200
REDIRECT_CODE = 302


class TaskTestCase(TestCase):
    """Test case class for tasks app."""

    def setUp(self):
        """Set up method for testing."""
        test_user = User.objects.create(
            username='test_user',
            password='test_pass',
        )
        test_status = Status.objects.create(
            name='test',
        )
        test_label = Label.objects.create(
            name='test',
        )
        test_task = Task.objects.create(
            name='test_task1',
            description='test',
            status=test_status,
            author=test_user,
        )
        test_task.labels.add(test_label)
        self.client.force_login(test_user)

    def test_tasks_list(self):
        """Test for checking tasks page."""
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='tasks/tasks_list.html')
        self.assertQuerysetEqual(
            response.context_data['object_list'],
            Task.objects.all(),
            ordered=False,
        )

    def test_create_task(self):
        """Test for checking task creation."""
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='tasks/task_create.html')
        response = self.client.post(reverse('create_task'), data={
            'name': 'test_task2',
            'description': 'test',
            'status': 1,
            'labels': 1,
        },
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task successfully created',
        )
        created_task = Task.objects.get(pk=2)
        self.assertEqual(response.status_code, REDIRECT_CODE)
        self.assertEqual('test_task2', created_task.name)
        self.assertEqual('test', created_task.description)
        self.assertEqual('test', created_task.status.name)
        self.assertEqual('test_user', created_task.author.username)
        self.assertEqual('test', created_task.labels.all()[0].name)

    def test_update_task(self):
        """Test for checking how task can be updated."""
        Status.objects.create(
            name='test_update',
        )
        response = self.client.get(reverse('update_task', args='1'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='tasks/task_update.html')
        response = self.client.post(reverse('update_task', args='1'), data={
            'name': 'test_update',
            'description': 'test_update',
            'status': 2,
            'executor': 1,
        },
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task successfully updated',
        )
        self.assertEqual(response.status_code, REDIRECT_CODE)
        self.assertEqual('test_update', Task.objects.get(pk=1).name)
        self.assertEqual('test_update', Task.objects.get(pk=1).description)
        self.assertEqual('test_update', Task.objects.get(pk=1).status.name)
        self.assertEqual('test_user', Task.objects.get(pk=1).executor.username)

    def test_delete_task(self):
        """Test for checking how status can be deleted."""
        response = self.client.get(reverse('delete_task', args='1'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='tasks/task_delete_confirm.html')
        response = self.client.post(reverse('delete_task', args='1'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task successfully deleted',
        )
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=1)

    def test_delete_not_own_task(self):
        """Test for checking that user can not delete other users tasks."""
        test_user2 = User.objects.create(
            username='test_user2',
            password='test_pass2',
        )
        Task.objects.create(
            name='test_task2',
            description='test2',
            status=Status.objects.get(pk=1),
            author=test_user2,
        )
        response = self.client.get(reverse('delete_task', args='2'))
        self.assertEqual(response.status_code, REDIRECT_CODE)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task can only be deleted by its author',
        )

    def test_detail_task_view(self):
        """Test for checking task details page."""
        test_task = Task.objects.get(pk=1)
        response = self.client.get(reverse('task_details', args='1'))
        self.assertEqual(response.status_code, OK_CODE)
        self.assertTemplateUsed(response, template_name='tasks/task_details.html')
        self.assertContains(response, test_task.name)
        self.assertContains(response, test_task.description)
        self.assertContains(response, test_task.author)
        self.assertContains(response, test_task.status)
        self.assertContains(response, test_task.labels.name)
