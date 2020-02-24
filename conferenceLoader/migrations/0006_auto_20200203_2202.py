# Generated by Django 2.2.5 on 2020-02-03 22:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conferenceLoader', '0005_auto_20200129_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date submitted'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='question',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date asked'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(default='', max_length=500),
        ),
    ]