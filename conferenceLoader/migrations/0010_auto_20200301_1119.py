# Generated by Django 2.2.5 on 2020-03-01 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferenceLoader', '0009_remove_feedback_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]