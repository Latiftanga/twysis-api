# Generated by Django 3.1 on 2020-08-18 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_class_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='name',
            new_name='division',
        ),
    ]
