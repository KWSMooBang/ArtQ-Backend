from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
import uuid

phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{9,15}$",
    message="Phone number should be 9~15 digits long."
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _clean_optional(self, value):
        # clean empty strings to None
        return value or None

    def create_user(self, username, password, nickname, email=None, phone_number=None, **extra_fields):
        if not username:
            raise ValueError("username field is necessary.")
        if not password:
            raise ValueError("password field is necessary.")
        if not nickname:
            raise ValueError("nickname field is necessary.")

        email = self.normalize_email(self._clean_optional(email))
        phone_number = self._clean_optional(phone_number)

        user = self.model(
            username=username,
            nickname=nickname,
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, nickname, email=None, phone_number=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser should have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser should have is_superuser=True.")

        return self.create_user(
            username=username,
            password=password,
            nickname=nickname,
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )

class User(AbstractUser):
    # user UUID as basic Public Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, validators=[phone_validator])
    birth_date = models.DateField(null=True, blank=True)
    
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # connect custom user manager
    objects = UserManager()

    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.nickname or self.username
