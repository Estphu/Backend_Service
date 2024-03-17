from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppViewSet, PlanViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'apps', AppViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]