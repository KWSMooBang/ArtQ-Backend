from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone
from datetime import date

class User(AbstractUser):
    # user UUID as basic Public Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, validators=[])
    full_name = models.CharField(max_length=150, null=True, blank=True)
    birth_date = models.DateField()
    nickname = models.CharField(max_length=20, unique=True, validators=[])
    
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'full_name', 'birth_date', 'nickname']
    
    def __str__(self):
        return self.username
    
    def clean(self):
        if self.birth_date:
            if self.birth_date < date(1900, 1, 1) or self.birth_date > timezone.now().date():
                raise ValueError("Invalid birth date.")
