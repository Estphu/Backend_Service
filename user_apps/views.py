from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import permissions
from .models import App, Plan, Subscription
from .serializers import AppSerializer, PlanSerializer, SubscriptionSerializer

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method filters the queryset based on the logged-in user.
        """
        user = self.request.user
        return App.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Creating a dictionary with the URLs for each App instance
        app_urls = {app['id']: request.build_absolute_uri(f"/api/apps/{app['id']}/") for app in data}

        # Updating the data with the URLs
        for app in data:
            app['url'] = app_urls[app['id']]

        return Response(data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method filters the queryset based on the logged-in user.
        """
        user = self.request.user
        return Plan.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Creating a dictionary with the URLs for each App instance
        plan_urls = {plan['id']: request.build_absolute_uri(f"/api/plans/{plan['id']}/") for plan in data}

        # Updating the data with the URLs
        for plan in data:
            plan['url'] = plan_urls[plan['id']]

        return Response(data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method filters the queryset based on the logged-in user.
        """
        user = self.request.user
        return Subscription.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Creating a dictionary with the URLs for each App instance
        sub_urls = {sub['id']: request.build_absolute_uri(f"/api/subscriptions/{sub['id']}/") for sub in data}

        # Updating the data with the URLs
        for sub in data:
            sub['url'] = sub_urls[sub['id']]

        return Response(data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)