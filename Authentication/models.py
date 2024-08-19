from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import random
import string

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Mobile Number"))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        expiry_duration = timezone.timedelta(minutes=10)
        return timezone.now() - self.created_at > expiry_duration

    def __str__(self):
        return f"OTP for {self.user.username}"
