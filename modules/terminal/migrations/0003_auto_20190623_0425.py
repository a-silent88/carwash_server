# Generated by Django 2.2.2 on 2019-06-23 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0002_auto_20190619_0754'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusTerminal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Статус терминала')),
            ],
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Статус сессии'),
        ),
        migrations.AddField(
            model_name='terminal',
            name='status',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='terminal.StatusTerminal'),
        ),
    ]