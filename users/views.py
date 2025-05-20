from rest_framework import viewsets
from .models import User, UserStatistics, Subscription, Wallet, RewardSystem, Streaming
from .serializers import UserSerializer, UserStatisticsSerializer, SubscriptionSerializer, WalletSerializer, RewardSystemSerializer, StreamingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserStatisticsViewSet(viewsets.ModelViewSet):
    queryset = UserStatistics.objects.all()
    serializer_class = UserStatisticsSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class RewardSystemViewSet(viewsets.ModelViewSet):
    queryset = RewardSystem.objects.all()
    serializer_class = RewardSystemSerializer

class StreamingViewSet(viewsets.ModelViewSet):
    queryset = Streaming.objects.all()
    serializer_class = StreamingSerializer
