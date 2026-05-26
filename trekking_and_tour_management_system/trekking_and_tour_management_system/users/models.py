from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None

    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("guide", "Guide"),
        ("admin", "Admin"),
    )

    name = CharField(
        _("Name of User"),
        max_length=255,
    )

    email = EmailField(
        _("email address"),
        unique=True,
    )

    role = CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer",
    )

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
    )
    must_change_password = models.BooleanField(
    default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    @property
    def is_customer(self):
        return self.role == "customer"

    @property
    def is_guide(self):
        return self.role == "guide"

    @property
    def is_admin_role(self):
        return self.role == "admin"

    def get_absolute_url(self) -> str:
        return reverse(
            "users:detail",
            kwargs={"pk": self.id},
        )

    def __str__(self):
        return self.email