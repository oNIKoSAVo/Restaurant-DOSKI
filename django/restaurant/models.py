from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Count
from functools import reduce

class PaymentTypes(models.IntegerChoices):
    ONLINE = 0, 'Онлайн оплата'
    CARD = 1, 'Картой'
    CASH = 2, 'Наличными'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    second_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    last_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    birthday = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=None)

    phone = models.CharField(max_length=16, blank=True,
                             null=True, default=None)
    registration_ip = models.GenericIPAddressField(default='192.168.0.1')

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        # app_label = 'auth'
        # db_table = 'restaurant_profile'
        


class Restaraunt(models.Model):
    address = models.CharField('Адрес', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)

    def __str__(self):
        return self.address + " " + self.phone

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

class RestarauntSchema(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, related_name='schemes', default=None, on_delete=models.DO_NOTHING)
    schema = models.FileField('Схема зала (SVG)', upload_to='tables/', blank=False, null=False)
    description = models.TextField('Описание', max_length=150, blank=False, null=False, default="")

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

class Category(models.Model):
    name = models.CharField('Категория', max_length=128, blank=False, null=False)
    parent = models.IntegerField('Родитель', blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

    @staticmethod
    def get_without(categories_skip = []):
        if(len(categories_skip) == 0):
            return Category.objects.all()
        not_display_categories_ids = []
        not_display_categories = Category.objects\
            .filter(
                reduce(lambda x, y: x | y, [Q(name=item) for item in categories_skip]))\

        not_display_categories_ids = [
            category.id for category in not_display_categories]

        for category_id in not_display_categories_ids:
            child = Category.objects.filter(parent=category_id)
            for c in child:
                    not_display_categories_ids.append(c.id)

        return Category.objects.exclude(id__in=not_display_categories_ids)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class Menue(models.Model):
    dish = models.CharField('Блюдо', max_length=128, blank=False, null=False)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='menues', on_delete=models.DO_NOTHING)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='menues', on_delete=models.DO_NOTHING)
    description = models.TextField('Описание', max_length=600, blank=False, null=False, default="")
    price = models.FloatField('Цена', blank=False, null=False, default=0)
    weight = models.CharField('Вес', max_length=128, blank=False, null=False, default="")
    image = models.ImageField('Изображение', upload_to='images/', blank=True, null=True, default="images/product.jpg")
    ident = models.IntegerField('Ident RKeeper',  blank=True, null=True)

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
    comment = models.TextField('Комментарий к заказу', max_length=128, blank=True, null=True)
    address = models.TextField('Адресс', max_length=300, blank=True, null=True)
    payment = models.IntegerField(
        'Тип оплаты', choices=PaymentTypes.choices, default=PaymentTypes.ONLINE)
    paid = models.BooleanField("Оплачено", blank=False, null=False, default=False)
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
    

class Feedback(models.Model):
    name = models.CharField('Имя', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)
    description = models.TextField('Отзыв', max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

class Franchising(models.Model):
    name = models.CharField('Имя', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'франшиза'
        verbose_name_plural = 'Франшиза'

class Сareer(models.Model):
    first_name = models.CharField('Имя', max_length=128, blank=False, null=False)
    middle_name = models.CharField('Отчество', max_length=128, blank=False, null=False)
    last_name = models.CharField('Фамилия', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)
    position = models.CharField('Должность', max_length=128, blank=False, null=False)
    city = models.CharField('Город', max_length=128, blank=False, null=False)
    bar = models.CharField('Бар', max_length=128, blank=False, null=False)
    b_day = models.DateField('Дата рождения', blank=False, null=False)
    citizenship = models.CharField('Гражданство', max_length=128, blank=False, null=False)
    about = models.TextField('О себе', max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'карьера'
        verbose_name_plural = 'Карьеры'

class Reservation(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='reservations', on_delete=models.DO_NOTHING, blank=False, null=False, default=0)
    start = models.DateTimeField('От', blank=False, null=False)
    end = models.DateTimeField('До', blank=False, null=False)
    persons = models.IntegerField('Кол-во человек', blank=False, null=False)
    table = models.IntegerField('Стол', blank=False, null=False)
    name = models.CharField('Имя', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон для связи', max_length=128, blank=False, null=False)
    description = models.TextField('Пожелание к брони', max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'бронь'
        verbose_name_plural = 'Бронирование'


class Event(models.Model):
    name = models.CharField('Название', max_length=128, blank=True, null=True)
    description = models.TextField('Описание', max_length=128, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='images/', blank=True, null=True)
    date = models.DateTimeField('Дата', blank=False, null=False)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'Событие'