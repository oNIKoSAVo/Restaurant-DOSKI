# Generated by Django 3.2.3 on 2021-12-24 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Категория')),
                ('parent', models.IntegerField(blank=True, null=True, verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Название города')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('instagram', models.CharField(blank=True, max_length=128, null=True, verbose_name='Ссылка на instagram')),
                ('vk', models.CharField(blank=True, max_length=128, null=True, verbose_name='Ссылка на ВК')),
            ],
            options={
                'verbose_name': 'город',
                'verbose_name_plural': 'города',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Имя')),
                ('phone', models.CharField(max_length=128, verbose_name='Телефон')),
                ('description', models.TextField(max_length=128, verbose_name='Отзыв')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Время изменения')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Franchising',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Имя')),
                ('phone', models.CharField(max_length=128, verbose_name='Телефон')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Время изменения')),
            ],
            options={
                'verbose_name': 'франшиза',
                'verbose_name_plural': 'Франшиза',
            },
        ),
        migrations.CreateModel(
            name='Menue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.CharField(max_length=128, verbose_name='Блюдо')),
                ('description', models.TextField(default='', max_length=600, verbose_name='Описание')),
                ('weight', models.CharField(default='', max_length=128, verbose_name='Вес')),
                ('image', models.ImageField(blank=True, default='images/product.jpg', null=True, upload_to='images/', verbose_name='Изображение')),
                ('ident', models.IntegerField(blank=True, null=True, verbose_name='Ident RKeeper')),
                ('is_drink', models.BooleanField(blank=True, null=True, verbose_name='Это напиток?')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='menues', to='restaurant.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'меню',
                'verbose_name_plural': 'меню',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=128, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'акции и новости',
                'verbose_name_plural': 'акции и новости',
            },
        ),
        migrations.CreateModel(
            name='Restaraunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=128, verbose_name='Телефон')),
                ('r_keeper', models.CharField(default='', max_length=255, verbose_name='R keeper login')),
                ('r_keeper_ip', models.CharField(default='', max_length=255, verbose_name='R keeper IP')),
                ('r_keeper_pass', models.CharField(default='', max_length=255, verbose_name='R keeper password')),
                ('ident', models.CharField(default='', max_length=255, verbose_name='Ident')),
                ('active_ident', models.CharField(default='', max_length=255, verbose_name='ActiveIdent')),
                ('price_ident', models.CharField(default='', max_length=255, verbose_name='PriceIdent')),
                ('start_available_ident', models.CharField(default='', max_length=255, verbose_name='StartAvailableIdent')),
                ('end_available_ident', models.CharField(default='', max_length=255, verbose_name='EndAvailableIdent')),
                ('coordinates', models.CharField(blank=True, max_length=255, null=True, verbose_name='Координаты')),
                ('yandex_eda', models.CharField(blank=True, max_length=128, null=True, verbose_name='Ссылка на яндекс еду')),
                ('menue_file', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='PDF Меню')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='restaraunts', to='restaurant.city', verbose_name='город')),
            ],
            options={
                'verbose_name': 'ресторан',
                'verbose_name_plural': 'рестораны',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oferta_file', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Оферта')),
                ('privacy_file', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Согласие на обработку персональных данных')),
            ],
            options={
                'verbose_name': 'настройки',
                'verbose_name_plural': 'настройки',
            },
        ),
        migrations.CreateModel(
            name='Сareer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=128, verbose_name='Отчество')),
                ('last_name', models.CharField(max_length=128, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=128, verbose_name='Телефон')),
                ('position', models.CharField(max_length=128, verbose_name='Должность')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
                ('bar', models.CharField(max_length=128, verbose_name='Бар')),
                ('b_day', models.DateField(verbose_name='Дата рождения')),
                ('citizenship', models.CharField(max_length=128, verbose_name='Гражданство')),
                ('about', models.TextField(max_length=128, verbose_name='О себе')),
            ],
            options={
                'verbose_name': 'карьера',
                'verbose_name_plural': 'Карьеры',
            },
        ),
        migrations.CreateModel(
            name='RestarauntSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema', models.FileField(upload_to='tables/', verbose_name='Схема зала (SVG)')),
                ('description', models.TextField(default='', max_length=150, verbose_name='Описание')),
                ('restaraunt', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='schemes', to='restaurant.restaraunt')),
            ],
            options={
                'verbose_name': 'ресторан',
                'verbose_name_plural': 'рестораны',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='От')),
                ('end', models.DateTimeField(verbose_name='До')),
                ('persons', models.IntegerField(verbose_name='Кол-во человек')),
                ('table', models.IntegerField(verbose_name='Стол')),
                ('name', models.CharField(max_length=128, verbose_name='Имя')),
                ('phone', models.CharField(max_length=128, verbose_name='Телефон для связи')),
                ('description', models.TextField(max_length=128, verbose_name='Пожелание к брони')),
                ('restaraunt', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reservations', to='restaurant.restaraunt', verbose_name='Ресторан')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'бронь',
                'verbose_name_plural': 'Бронирование',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('second_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('birthday', models.DateField(blank=True, default=None, null=True)),
                ('phone', models.CharField(blank=True, default=None, max_length=16, null=True)),
                ('email', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('registration_ip', models.GenericIPAddressField(default='192.168.0.1')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
        migrations.CreateModel(
            name='PreOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Сумма предзаказа')),
                ('comment', models.TextField(blank=True, max_length=128, null=True, verbose_name='Комментарий к предзаказу')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='restaurant.reservation', verbose_name='Резерв')),
                ('restaraunt', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='preorders', to='restaurant.restaraunt', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'предзаказ',
                'verbose_name_plural': 'Предзаказы',
            },
        ),
        migrations.CreateModel(
            name='PhotoTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.ImageField(upload_to='images/', verbose_name='фото стола')),
                ('table_number', models.IntegerField(verbose_name='Номер стола')),
                ('restaraunt', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.restaraunt', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Фото стола',
                'verbose_name_plural': 'Фото столов',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Сумма заказа')),
                ('comment', models.TextField(blank=True, max_length=128, null=True, verbose_name='Комментарий к заказу')),
                ('address', models.TextField(blank=True, max_length=300, null=True, verbose_name='Адресс')),
                ('payment', models.IntegerField(choices=[(0, 'Онлайн оплата'), (1, 'Картой'), (2, 'Наличными')], default=0, verbose_name='Тип оплаты')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('restaraunt', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='restaurant.restaraunt', verbose_name='Ресторан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='MenuInPreOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menue', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.menue', verbose_name='Меню')),
                ('preorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menues', to='restaurant.preorder', verbose_name='Предзаказ')),
            ],
        ),
        migrations.CreateModel(
            name='MenuInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menue', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.menue', verbose_name='Меню')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='menues', to='restaurant.order', verbose_name='Заказ')),
            ],
        ),
        migrations.CreateModel(
            name='MenueInRestaraunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('menue', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='in_restaraunt', to='restaurant.menue', verbose_name='Меню')),
                ('restaraunt', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='in_menue', to='restaurant.restaraunt', verbose_name='Ресторан')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=128, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.city', verbose_name='Город')),
                ('restaraunt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.restaraunt', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'событие',
                'verbose_name_plural': 'Событие',
            },
        ),
    ]
