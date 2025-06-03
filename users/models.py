# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # one org per user ‑– switch to ManyToManyField if you need many‑to‑many
    organization = models.ForeignKey(
        Organization,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
    )

class PlainUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)  # ⚠️ stored in plain text

    def __str__(self):
        return self.username
