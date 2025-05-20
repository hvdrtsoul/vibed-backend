from rest_framework import serializers
from .models import User, UserStatistics, Subscription, Wallet, RewardSystem, Streaming

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'wallet_address', 'username', 'email', 'is_verified']

class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistics
        fields = ['user', 'total_plays', 'total_rewards', 'total_subscribes', 'active_subscriptions']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'start_date', 'end_date', 'is_active', 'subscription_type']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']

class RewardSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardSystem
        fields = ['user', 'amount', 'date']

class StreamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streaming
        fields = ['user', 'track_id', 'start_time', 'end_time']
