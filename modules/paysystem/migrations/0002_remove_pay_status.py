# Generated by Django 2.2.2 on 2019-06-18 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paysystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pay',
            name='status',
        ),
    ]
