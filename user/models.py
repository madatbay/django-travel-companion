from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.html import mark_safe


class UserManager(BaseUserManager):
    """User Manager that knows how to create users via email instead of username"""

    def _create_user(self, email, password, username="", **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    full_name = models.CharField("Full name", max_length=80, help_text="Max length: 80 sumbols")
    email = models.EmailField("Email", unique=True, max_length=120, help_text="Max length: 120 symbols")
    password = models.CharField("Password", max_length=120, help_text="Max length: 80 symbols")
    avatar = models.ImageField(
        upload_to="users/",
        max_length=255,
        null=True,
        blank=True,
        help_text="Recommended size: 1080x1080px",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    @property
    def avatar_preview(self):
        if self.avatar:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.avatar.url))
        return "Not set"

    def __str__(self):
        return "{}".format(self.email)

    def __repr__(self) -> str:
        return f"[{self.email}]"

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
