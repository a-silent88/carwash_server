# Generated by Django 2.2.2 on 2020-08-20 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paysystem', '0007_auto_20200820_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incas',
            name='date',
            field=models.DateTimeField(verbose_name='Дата инкассации'),
        ),
    ]
