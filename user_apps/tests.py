from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import App, Plan, Subscription

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import App, Plan, Subscription
from .serializers import AppSerializer

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import App, Plan, Subscription
from .serializers import AppSerializer

class AppViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.free_plan = Plan.objects.create(name='Free', price=0)

    def test_create_app(self):
        """
        Test creating an app through the API.
        """
        url = '/api/apps/'
        data = {
            'name': 'Test App',
            'description': 'This is a test app'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        app = App.objects.get(name='Test App')
        self.assertEqual(app.user, self.user)
        self.assertEqual(app.name, 'Test App')
        self.assertEqual(app.description, 'This is a test app')

        # Check if a subscription was created with the Free Plan
        subscription = Subscription.objects.get(app=app)
        self.assertEqual(subscription.plan, self.free_plan)
        self.assertTrue(subscription.active)

    def test_list_apps(self):
        """
        Test retrieving a list of apps through the API.
        """
        # Create some sample apps
        App.objects.create(name='App 1', description='Description 1', user=self.user)
        App.objects.create(name='App 2', description='Description 2', user=self.user)

        url = '/api/apps/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_app(self):
        """
        Test updating an existing app through the API.
        """
        app = App.objects.create(name='Old App', description='Old Description', user=self.user)
        url = f'/api/apps/{app.id}/'
        data = {
            'name': 'New App',
            'description': 'New Description'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the app was updated
        app.refresh_from_db()
        self.assertEqual(app.name, 'New App')
        self.assertEqual(app.description, 'New Description')

    def test_delete_app(self):
        """
        Test deleting an app through the API.
        """
        app = App.objects.create(name='App to Delete', description='App to Delete Description', user=self.user)
        url = f'/api/apps/{app.id}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the app was deleted
        with self.assertRaises(App.DoesNotExist):
            App.objects.get(id=app.id)

class PlanViewSetTest(APITestCase):

    def setUp(self):
        self.client.login(username='admin', password='adminpass')

    def test_list_plans(self):
        Plan.objects.create(name='Free Plan', price=0)
        Plan.objects.create(name='Standard Plan', price=10)
        Plan.objects.create(name='Pro Plan', price=25)

        response = self.client.get('/api/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_plan(self):
        data = {
            'name': 'New Plan',
            'price': 15
        }
        response = self.client.post('/api/plans/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(Plan.objects.first().name, 'New Plan')
        self.assertEqual(Plan.objects.first().price, 15)

    def test_update_plan(self):
        plan = Plan.objects.create(name='Free Plan', price=0)
        data = {
            'name': 'Updated Plan',
            'price': 5
        }
        response = self.client.put(f'/api/plans/{plan.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.name, 'Updated Plan')
        self.assertEqual(plan.price, 5)

    def test_delete_plan(self):
        plan = Plan.objects.create(name='Free Plan', price=0)
        response = self.client.delete(f'/api/plans/{plan.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Plan.objects.count(), 0)

class SubscriptionViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.app = App.objects.create(name='Test App', description='Test Description', user=self.user)
        self.plan = Plan.objects.create(name='Free Plan', price=0)
        self.subscription = Subscription.objects.create(app=self.app, plan=self.plan)

    def test_list_subscriptions(self):
        response = self.client.get('/api/subscriptions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_subscription(self):
        data = {
            'app': self.app.id,
            'plan': self.plan.id
        }
        response = self.client.post('/api/subscriptions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 2)

    def test_update_subscription(self):
        new_plan = Plan.objects.create(name='Standard Plan', price=10)
        data = {
            'plan': new_plan.id
        }
        response = self.client.put(f'/api/subscriptions/{self.subscription.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.plan, new_plan)

    def test_delete_subscription(self):
        response = self.client.delete(f'/api/subscriptions/{self.subscription.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)        