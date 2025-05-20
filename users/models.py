from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from phantom_auth.models import PhantomUser as User

class UserStatistics(models.Model):
    user = models.OneToOneField(User, related_name='statistics', on_delete=models.CASCADE)
    total_plays = models.IntegerField(default=0)
    total_rewards = models.FloatField(default=0)
    total_subscribes = models.IntegerField(default=0)
    active_subscriptions = models.IntegerField(default=0)

    def __str__(self):
        return f"Statistics for {self.user.username}"

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    subscription_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Subscription for {self.user.username}"

class Wallet(models.Model):
    user = models.OneToOneField(User, related_name='wallet', on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"Wallet for {self.user.username}"

class RewardSystem(models.Model):
    user = models.ForeignKey(User, related_name='rewards', on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reward for {self.user.username}"

class Streaming(models.Model):
    user = models.ForeignKey(User, related_name='streams', on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Stream for {self.user.username} with track {self.track_id}"
