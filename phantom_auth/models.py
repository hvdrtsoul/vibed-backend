from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class PhantomUserManager(BaseUserManager):
    def create_user(self, public_key, password=None):
        if not public_key:
            raise ValueError("User must have a public_key")
        user = self.model(public_key=public_key)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, public_key, password=None):
        user = self.create_user(public_key, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class PhantomUser(AbstractBaseUser, PermissionsMixin):
    public_key = models.CharField(max_length=128, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PhantomUserManager()

    USERNAME_FIELD = 'public_key'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.public_key
class PhantomNonce(models.Model):
    public_key = models.CharField(max_length=128, unique=True)
    nonce = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        return timezone.now() - self.created_at > timedelta(minutes=5)