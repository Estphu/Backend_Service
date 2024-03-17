from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm

class HomeViewTest(TestCase):

    def test_home_view(self):
        response = self.client.get(reverse('users:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

class RegisterViewTest(TestCase):

    def test_register_view_get(self):
        response = self.client.get(reverse('users:user-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_view_post_valid_form(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('users:user-register'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to login page on successful registration
        self.assertRedirects(response, reverse('login'))

    def test_register_view_post_invalid_form(self):
        data = {}  # Invalid form data
        response = self.client.post(reverse('users:user-register'), data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

class CustomLoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_custom_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_custom_login_view_post(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'remember_me': False,
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to home page on successful login
        self.assertRedirects(response, reverse('users:home'))

    def test_custom_login_view_post_remember_me(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'remember_me': True,
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to home page on successful login
        self.assertRedirects(response, reverse('users:home'))


class ChangePasswordViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpassword')
        self.client.login(username='testuser', password='oldpassword')

    def test_change_password_view_get(self):
        response = self.client.get(reverse('password-change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_password.html')

    def test_change_password_view_post(self):
        data = {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        }
        response = self.client.post(reverse('password-change'), data)
        print(response.status_code)
        self.assertEqual(response.status_code, 302)  # Redirects to success url on successful password change
        self.assertRedirects(response, reverse('users:home')) # Checking for successful redirection to the expected URL
        self.assertTrue(self.client.login(username='testuser', password='newpassword')) # Ensuring the user can still logged in after password change