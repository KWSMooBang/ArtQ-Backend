from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import uuid

phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{9,15}$",
    message="Phone number should be 9~15 digits long."
)

class User(AbstractUser):
    # user UUID as basic Public Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, validators=[phone_validator])
    birth_date = models.DateField()
    nickname = models.CharField(max_length=30)
    
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'full_name', 'birth_date', 'nickname']
    
    def __str__(self):
        return self.username
