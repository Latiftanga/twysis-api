# Generated by Django 3.1 on 2020-08-15 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200815_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='division',
        ),
    ]
