from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_create_user(self):
        response = self.client.post(reverse('user_create'), {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'username': 'iivan',
            'password': 'mypass',
            'confirm_password': 'mypass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='iivan').exists())

    def test_update_user(self):
        response = self.client.post(reverse(
            'user_update', 
            kwargs={'id': self.user.id}),
            {'first_name': 'Semyon',
                'last_name': self.user.last_name,
                'username': self.user.username,
                'password': self.user.password,
                'confirm_password': self.user.password
            })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, "Semyon")

    def test_update_user_fail_password_confirmation(self):
        response = self.client.post(reverse('user_update', 
                                            kwargs={'id': self.user.id}),
                                            {'first_name': 'Eddy',
                                             'last_name': self.user.last_name,
                                             'username': self.user.username,
                                             'password': self.user.password,
                                             'confirm_password': 'wrongpass'
                                            })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.post(reverse("user_delete", 
                                            kwargs={'id': self.user.id,
                                                    }))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())