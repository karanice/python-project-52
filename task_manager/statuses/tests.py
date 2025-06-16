from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Status

User = get_user_model()


class StatusTest(TestCase):

    fixtures = ['users.json', 'statuses.json']
    
    def setUp(self):
        self.user = User.objects.first()
        self.status = Status.objects.first()
        self.client.force_login(self.user)

    def test_create_status(self):
        response = self.client.post(reverse('status_create'), {
            'name': 'Waiting',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Waiting').exists())

    def test_update_status(self):
        response = self.client.post(reverse('status_update',
                                            kwargs={'pk': self.status.pk}),
                                            {'name': 'New Name',
                                            })
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "New Name")
        self.assertEqual(response.status_code, 302)

    def test_delete_status(self):
        response = self.client.post(reverse("status_delete", 
                                            kwargs={'pk': self.status.pk,
                                                    }))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        self.assertEqual(response.status_code, 302)
