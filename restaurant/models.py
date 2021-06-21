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
        app_label = 'auth'
        db_table = 'restaurant_profile'
        


class Restaraunt(models.Model):
    address = models.CharField('Адрес', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)
    schema = models.CharField('Схема зала', max_length=128, blank=False, null=False)

    def __str__(self):
        return self.address + " " + self.phone

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

class Category(models.Model):
    name = models.CharField('Категория', max_length=128, blank=False, null=False)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class Menue(models.Model):
    dish = models.CharField('Блюдо', max_length=128, blank=False, null=False)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='menues', on_delete=models.DO_NOTHING)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='menues', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.category.name + " | " + self.dish

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders',
                              on_delete=models.CASCADE, blank=False, null=False)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='orders', on_delete=models.DO_NOTHING,  blank=False, null=False)
    price = models.FloatField('Сумма заказа', blank=False, null=False, default=0)

    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Время изменения', auto_now=True)

    def __str__(self):
        return "Заказ #%s" % self.id

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

class MenuInOrder(models.Model):
    menue = models.ForeignKey(Menue, verbose_name='Меню', on_delete=models.DO_NOTHING, blank=False, null=False)
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='menues', on_delete=models.DO_NOTHING, blank=False, null=False)

    def __str__(self) -> str:
        return "%s" % self.menue
    