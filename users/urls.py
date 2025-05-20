from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserStatisticsViewSet, SubscriptionViewSet, WalletViewSet, RewardSystemViewSet, StreamingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-statistics', UserStatisticsViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'rewards', RewardSystemViewSet)
router.register(r'streaming', StreamingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
