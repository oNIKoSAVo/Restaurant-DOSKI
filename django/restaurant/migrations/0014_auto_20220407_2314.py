# Generated by Django 3.2.9 on 2022-04-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_setting_payment_and_return'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Сareer',
            new_name='Career',
        ),
        migrations.AddField(
            model_name='setting',
            name='career_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='почта для отправки анкет по карьере'),
        ),
        migrations.AddField(
            model_name='setting',
            name='feedback_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='почта для отправки отзывов'),
        ),
        migrations.AddField(
            model_name='setting',
            name='franchising_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='почта для заявок на франшизу'),
        ),
    ]
