# Generated by Django 2.2.2 on 2020-08-20 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paysystem', '0008_auto_20200820_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='status',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='paysystem.StatusPay'),
        ),
    ]
