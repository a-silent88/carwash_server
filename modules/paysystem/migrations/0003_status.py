# Generated by Django 2.2.2 on 2019-06-18 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paysystem', '0002_remove_pay_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Статус')),
            ],
        ),
    ]