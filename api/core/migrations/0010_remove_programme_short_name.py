# Generated by Django 3.1 on 2020-08-14 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_class_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programme',
            name='short_name',
        ),
    ]
