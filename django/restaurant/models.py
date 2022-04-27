from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Count
from functools import reduce
from django.core.validators import FileExtensionValidator
from restaurant.lib.sms import Sms
from timezone_field import TimeZoneField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from ckeditor.fields import RichTextField


class PaymentTypes(models.IntegerChoices):
    ONLINE = 0, 'Онлайн оплата'
    CARD = 1, 'Картой'
    CASH = 2, 'Наличными'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_deleted = models.BooleanField(blank=True, default=False)
    first_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    second_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    last_name = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    birthday = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=None)

    phone = models.CharField(max_length=16, blank=True,
                             null=True, default=None)
    email = models.CharField(
        max_length=128, blank=True, null=True, default=None)
    registration_ip = models.GenericIPAddressField(default='192.168.0.1')
    is_password_changed = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        # app_label = 'auth'
        # db_table = 'restaurant_profile'

class City(models.Model):
    name = models.CharField('Название города', max_length=128, blank=True, null=True)
    phone = models.CharField('Номер телефона', max_length=20, blank=True, null=True)
    instagram = models.CharField('Ссылка на instagram', max_length=128, blank=True, null=True)
    vk = models.CharField('Ссылка на ВК', max_length=128, blank=True, null=True)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
#     restaraunts = models.ManyToManyField('self', blank=True, related_name='Restaraunt', )
    city_timezone = TimeZoneField(verbose_name="Временная зона", choices_display="WITH_GMT_OFFSET", null=True, blank=True)

    def __str__(self):
       return self.name

    class Meta:
            verbose_name = 'город'
            verbose_name_plural = 'города'

class Restaraunt(models.Model):
    address = models.CharField('Адрес', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)
    r_keeper = models.CharField('R keeper login', max_length=255, blank=False, null=False, default="")
    r_keeper_ip = models.CharField('R keeper IP', max_length=255, blank=False, null=False, default="")
    r_keeper_pass = models.CharField('R keeper password', max_length=255, blank=False, null=False, default="")
    ident = models.CharField('Ident', help_text='PropTRADEGROUPS > Property[Ident]', max_length=255, blank=False, null=False, default="")
    active_ident = models.CharField('ActiveIdent', max_length=255, blank=False, null=False, default="")  #нигде не используется
    price_ident = models.CharField('PriceIdent', help_text='PropPRICETYPES > Property[Ident]', max_length=255, blank=False, null=False, default="")
    start_available_ident = models.CharField('StartAvailableIdent', max_length=255, blank=False, null=False, default="")
    end_available_ident = models.CharField('EndAvailableIdent', max_length=255, blank=False, null=False, default="")
    coordinates=models.CharField('Координаты', max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='город', related_name='restaraunts', on_delete=models.DO_NOTHING, blank=True, null=True)
    yandex_eda = models.CharField('Ссылка на яндекс еду', max_length=128, blank=True, null=True)
    menue_file = models.FileField('PDF Меню', upload_to='images/', blank=True, null=True)

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
    description = models.TextField('Описание', max_length=600, blank=False, null=False, default="")
    weight = models.CharField('Вес', max_length=128, blank=False, null=False, default="")
    # image = models.ImageField('Изображение', upload_to='images/', blank=True, null=True, default="images/product.jpg")
    image = ProcessedImageField(verbose_name="Изображение",
                                upload_to='images/',
                                processors=[ResizeToFit(400, 300)],
                                format='JPEG',
                                options={'quality': 90},
                                blank=True,
                                null=True)
                                
    ident = models.IntegerField('Ident RKeeper',  blank=True, null=True)
    is_drink = models.BooleanField('Это напиток?',  blank=True, null=True)
    is_active = models.BooleanField('Активен?',  blank=True, null=False, default=True)

    def __str__(self):
        return self.category.name + " | " + self.dish

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'

class MenueInRestaraunt(models.Model):
    menue =  models.ForeignKey(Menue, verbose_name='Меню', related_name='in_restaraunt', on_delete=models.DO_NOTHING)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='in_menue', on_delete=models.DO_NOTHING)
    price = models.FloatField('Цена', blank=False, null=False, default=0)
    start_time = models.TimeField('Время доступности ОТ', blank=True, null=True)
    end_time = models.TimeField('Время доступности ДО', blank=True, null=True)
    stop_list = models.BooleanField('Стоп лист', blank=True, null=True, default=False)

class OrderStatusType(models.IntegerChoices):
    WAIT = 0, 'В ожидании'
    APPROVED = 1, 'Подтвержден'
    REJECT = 2, 'Отклонен'

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders',
                              on_delete=models.DO_NOTHING, blank=False, null=False)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='orders', on_delete=models.DO_NOTHING,  blank=False, null=False)
    price = models.FloatField('Сумма заказа', blank=False, null=False, default=0)
    comment = models.TextField('Комментарий к заказу', max_length=128, blank=True, null=True)
    address = models.TextField('Адресс', max_length=300, blank=True, null=True)
    payment = models.IntegerField(
        'Тип оплаты', choices=PaymentTypes.choices, default=PaymentTypes.ONLINE)
    paid = models.BooleanField("Оплачено", blank=False, null=False, default=False)
    status = models.IntegerField('Статус', choices=OrderStatusType.choices, null=True, default=OrderStatusType.WAIT)
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
    created_at = models.DateTimeField('Время создания', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Время изменения', auto_now=True, null=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

class Franchising(models.Model):
    name = models.CharField('Имя', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон', max_length=128, blank=False, null=False)
    created_at = models.DateTimeField('Время создания', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Время изменения', auto_now=True, null=True)

    class Meta:
        verbose_name = 'франшиза'
        verbose_name_plural = 'Франшиза'

class Career(models.Model):
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

class ReservationStatusType(models.IntegerChoices):
    WAIT = 0, 'В ожидании'
    APPROVED = 1, 'Подтверждена'
    REJECT = 2, 'Отклонена'

class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations',
                              on_delete=models.CASCADE, blank=True, null=True)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='reservations', on_delete=models.DO_NOTHING, blank=False, null=False, default=0)
    start = models.DateTimeField('От', blank=False, null=False)
    end = models.DateTimeField('До', blank=False, null=False)
    persons = models.IntegerField('Кол-во человек', blank=False, null=False)
    table = models.IntegerField('Стол', blank=False, null=False)
    name = models.CharField('Имя', max_length=128, blank=False, null=False)
    phone = models.CharField('Телефон для связи', max_length=128, blank=False, null=False)
    description = models.TextField('Пожелание к брони', max_length=128, blank=False, null=False)
    status = models.IntegerField('Статус', choices=ReservationStatusType.choices, null=True, default=ReservationStatusType.WAIT)

    class Meta:
        verbose_name = 'бронь'
        verbose_name_plural = 'Бронирование'


class Event(models.Model):
    name = models.CharField('Название', max_length=128, blank=True, null=True)
    description = models.TextField('Описание', max_length=128, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='images/', blank=True, null=True)
    date = models.DateTimeField('Дата', blank=False, null=False)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', on_delete=models.DO_NOTHING, blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'Событие'

class Promotion(models.Model):
    name = models.CharField('Название', max_length=128, blank=True, null=True)
    description = models.TextField('Описание', max_length=128, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='images/', blank=True, null=True)

    class Meta:
        verbose_name = 'акции и новости'
        verbose_name_plural = 'акции и новости'

class PreOrder(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='preorders', on_delete=models.DO_NOTHING,  blank=False, null=False)
    reservation = models.ForeignKey(Reservation, verbose_name='Резерв', related_name='reservation', on_delete=models.CASCADE,  blank=True, null=True)
    price = models.FloatField('Сумма предзаказа', blank=False, null=False, default=0)
    comment = models.TextField('Комментарий к предзаказу', max_length=128, blank=True, null=True)
    filepdf = models.FileField('Файл предзаказа', upload_to='preorders/', blank=True, null=True)
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Время изменения', auto_now=True)

    def __str__(self):
        return "Заказ #%s" % self.id

    class Meta:
        verbose_name = 'предзаказ'
        verbose_name_plural = 'Предзаказы'

class MenuInPreOrder(models.Model):
    menue = models.ForeignKey(Menue, verbose_name='Меню', on_delete=models.DO_NOTHING, blank=False, null=False)
    preorder = models.ForeignKey(PreOrder, verbose_name='Предзаказ', related_name='menues', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self) -> str:
        return "%s" % self.menue


class Setting(models.Model):
    oferta_file = models.FileField('Оферта', upload_to='images/', blank=True, null=True)
    privacy_file = models.FileField('Согласие на обработку персональных данных', upload_to='images/', blank=True, null=True)
    main_banner = models.ImageField('Главный баннер на странице', upload_to='images/', blank=True, null=True)
    main_banner_mobile = models.ImageField('Баннер на главной странице в мобильной версии', upload_to='images/', blank=True, null=True)
    career_video = models.FileField('Видео на странице карьеры',
                                    upload_to='videos/', 
                                    validators=[
                                        FileExtensionValidator(
                                            allowed_extensions=['mp3', 'mp4', 'avi', 'ogg', 'webm']
                                        )
                                    ],
                                    blank=True, 
                                    null=True)

    payment_and_return = RichTextField('Оплата и возврат', max_length=5000, null=True, blank=True)
    allow_period_reservation = models.IntegerField('Доступный период бронирования (+ дней)',  blank=True, null=True)

    # RESERVATION FIELDS:
    allow_time_reservation_start = models.TimeField('Доступное время бронирования(вск-чтв)', help_text="С",  blank=True, null=True)
    allow_time_reservation_end = models.TimeField('Доступное время бронирования(вск-чтв)', help_text="ДО",  blank=True, null=True)

    allow_weekend_time_reservation_start = models.TimeField('Доступное время бронирования(птн-сб)', help_text="С",  blank=True, null=True)
    allow_weekend_time_reservation_end = models.TimeField('Доступное время бронирования(птн-сб)', help_text="ДО",  blank=True, null=True)
    # ____________________

    allow_time_delivery_start = models.TimeField('Доступное время доставки', help_text="С",  blank=True, null=True)
    allow_time_delivery_end = models.TimeField('Доступное время доставки', help_text="ДО",  blank=True, null=True)

    franchising_email = models.CharField('почта для заявок на франшизу', 
                                         max_length=255,
                                         null=True, 
                                         blank=True)
    career_email = models.CharField('почта для отправки анкет по карьере', 
                                    max_length=255,
                                    null=True, 
                                    blank=True)
    feedback_email = models.CharField('почта для отправки отзывов', 
                                      max_length=255,
                                      null=True, 
                                      blank=True)

    class Meta:
        verbose_name = 'настройки'
        verbose_name_plural = 'настройки'

class PhotoTable(models.Model):
    table = models.ImageField('фото стола', upload_to='images/', blank=False, null=False)
    table_number = models.IntegerField('Номер стола',  blank=False, null=False)
    restaraunt = models.ForeignKey(Restaraunt, verbose_name='Ресторан', related_name='tables', on_delete=models.DO_NOTHING, blank=False, null=False)
    description = models.TextField('Описание стола', max_length=128, blank=False, null=False, default="")

    class Meta:
        verbose_name = 'Фото стола'
        verbose_name_plural = 'Фото столов'

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Reservation)
def update_reservation(sender, instance, **kwargs):
    if(instance.status == ReservationStatusType.REJECT):
       Sms().send(phone=instance.phone, message="Бронирование отменено.")