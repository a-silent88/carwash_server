# Generated by Django 2.2.2 on 2020-06-24 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0010_usage_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='balance',
            field=models.IntegerField(blank=True, default=0, max_length=20, null=True, verbose_name='Баланс'),
        ),
    ]