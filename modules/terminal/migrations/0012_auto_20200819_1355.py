# Generated by Django 2.2.2 on 2020-08-19 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0011_auto_20200624_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='balance',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Баланс'),
        ),
    ]
