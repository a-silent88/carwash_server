# Generated by Django 2.2.2 on 2020-08-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_customuser_cardid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
