from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.accounts.managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    company = models.CharField(max_length=255, null=True, blank=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, db_index=True)
    is_active = models.BooleanField('active', default=True)

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = AccountManager()

    @property
    def is_staff(self):
        return self.is_superuser
