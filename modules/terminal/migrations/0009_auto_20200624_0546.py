# Generated by Django 2.2.2 on 2020-06-24 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0008_auto_20200623_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='balance',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Баланс'),
        ),
    ]