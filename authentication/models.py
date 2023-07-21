from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.conf import settings
import jwt
from datetime import datetime, timedelta

from client_app.models import *


# hello this is Zacky project
class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("Username must be set")
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_(
            "Designates whether this user has verified their email on sign up. "
        ),
    )

    first_name = models.CharField(_("first name"), max_length=255, blank=False)
    last_name = models.CharField(_("last name"), max_length=255, blank=False)
    phone_number = models.CharField(_("phone number"), max_length=13, blank=False)

    # options (super_Admin, admin, user)
    USER_CHOICES = [
        ("Superadmin", _("Superadmin")),
        ("Admin", _("Admin")),
        ("User", _("User")),
    ]

    # user type
    user_type = models.CharField(
        _("user type"), max_length=255, choices=USER_CHOICES, blank=False
    )

    # options (active, not active)
    STATUS_CHOICES = [
        ("Active", _("Active")),
        ("Inactive", _("Inactive")),
    ]

    # user status
    user_status = models.CharField(
        _("user status"), max_length=15, choices=STATUS_CHOICES, blank=False
    )

    property = models.CharField(_("property"), max_length=15, blank=True, null=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # created at
    created_at = models.DateTimeField(_("created at"), default=timezone.now)

    # updated at
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def token(self):
        token = jwt.encode(
            {
                "username": self.username,
                "email": self.email,
                "exp": datetime.utcnow() + timedelta(hours=12),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token
