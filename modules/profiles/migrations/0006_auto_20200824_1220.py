# Generated by Django 2.2.2 on 2020-08-24 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_customuser_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
