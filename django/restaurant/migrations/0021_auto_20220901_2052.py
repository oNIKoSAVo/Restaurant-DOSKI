# Generated by Django 3.2.9 on 2022-09-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0020_auto_20220901_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaraunt',
            name='payment_key',
            field=models.CharField(default='Nzk1MjkwNTY3MDY6ZDVkOThiYzI0YWZjMmM1OTNkOGEzMjMzOGJhZmI3ZmY=', max_length=255, verbose_name='Ключ терминала для оплаты'),
        ),
        migrations.AlterField(
            model_name='restaraunt',
            name='payment_terminal_id',
            field=models.CharField(default='9a73af7faff347bf8844c66d8333ae84', max_length=255, verbose_name='ИД терминала для оплаты'),
        ),
    ]
