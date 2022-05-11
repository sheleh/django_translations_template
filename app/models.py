from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from app.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    language = models.CharField(max_length=2, blank=True, verbose_name=_('language'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
