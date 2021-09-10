# Generated by Django 3.2.3 on 2021-09-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_auto_20210908_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Адресс'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.IntegerField(choices=[(0, 'Онлайн оплата'), (1, 'Картой'), (2, 'Наличными')], default=0, verbose_name='Тип оплаты'),
        ),
    ]