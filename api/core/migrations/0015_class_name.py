# Generated by Django 3.1 on 2020-08-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_class_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='name',
            field=models.CharField(default='A', max_length=16),
            preserve_default=False,
        ),
    ]
