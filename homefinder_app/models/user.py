from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from django.utils import timezone

from homefinder_app.enums import Gender, Role


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.admin.name)  # ← вот это ключевая строка

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    role = models.CharField(
        max_length=20,
        choices=Role.choices(),
        default=Role.tenant.name
    )

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices(),
        null=True,
        blank=True
    )

    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email