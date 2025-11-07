from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    budget = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=120, null=True, blank=True)
    interests = models.JSONField(default=list, blank=True)
