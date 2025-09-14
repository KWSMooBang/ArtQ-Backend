from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    # user UUID as basic Public Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=30, unique=True)
    
    profile_image_url = models.URLField(blank=True, null=True)
    prefs = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return self.nickname or self.username
