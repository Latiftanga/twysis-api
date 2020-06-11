# Generated by Django 3.1a1 on 2020-06-11 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200603_1750'),
        ('students', '0011_auto_20200610_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.school'),
            preserve_default=False,
        ),
    ]
