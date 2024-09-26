from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.

class AuthTests(TestCase):
    def test_user_can_register(self):
        response = self.client.post('/register/', {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_user_can_login(self):
        User.objects.create_user('testuser', password='password123')
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login success
