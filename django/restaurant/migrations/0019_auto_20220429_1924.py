# Generated by Django 3.2.9 on 2022-04-29 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0018_auto_20220427_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='priority',
            field=models.IntegerField(blank=True, default=0, verbose_name='Приоритет'),
        ),
        migrations.AddField(
            model_name='setting',
            name='main_topslider_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Заголовок на главной в секции новости и акции'),
        ),
    ]
