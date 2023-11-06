from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(verbose_name="Аватар", blank=True, null=True, upload_to="avatars")
    phone_number = models.CharField(verbose_name="Phone", max_length=100, blank=True, null=True)
    @property
    def text(self):
        return self.last_name if self.last_name else self.username

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'