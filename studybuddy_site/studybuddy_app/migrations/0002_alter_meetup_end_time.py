# Generated by Django 4.2.2 on 2023-06-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studybuddy_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end time'),
        ),
    ]