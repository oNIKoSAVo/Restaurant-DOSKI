from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    second_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    last_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    birthday = models.DateField(auto_now=False, auto_now_add=False)

    phone = models.CharField(max_length=16, blank=True,
                             null=True, default=None)
    registration_ip = models.GenericIPAddressField(default='192.168.0.1')

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class Restaraunt(models.Model):
    address = models.CharField('Адрес', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)
    schema = models.CharField('Схема зала', max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class Menue(models.Model):
    dish = models.CharField('Блюдо',max_length=128, blank=False, null=False)
    category = models.CharField('Категория',max_length=128, blank=False, null=False)
    restaraunt = models.OneToOneField(Restaraunt, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'
