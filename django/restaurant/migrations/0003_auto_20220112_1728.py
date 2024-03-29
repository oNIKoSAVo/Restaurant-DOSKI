# Generated by Django 3.2.3 on 2022-01-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20220110_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='menueinrestaraunt',
            name='stop_list',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Стоп лист'),
        ),
        migrations.AlterField(
            model_name='restaraunt',
            name='ident',
            field=models.CharField(default='', help_text='PropTRADEGROUPS > Property[Ident]', max_length=255, verbose_name='Ident'),
        ),
        migrations.AlterField(
            model_name='restaraunt',
            name='price_ident',
            field=models.CharField(default='', help_text='PropPRICETYPES > Property[Ident]', max_length=255, verbose_name='PriceIdent'),
        ),
    ]
