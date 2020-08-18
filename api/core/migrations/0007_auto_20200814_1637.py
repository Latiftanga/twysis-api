# Generated by Django 3.1 on 2020-08-14 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='year',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='level',
            field=models.CharField(choices=[('PRIMARY', 'Primary'), ('JHS', 'Junior High'), ('SHS', 'Senior High')], default='SHS', max_length=8),
            preserve_default=False,
        ),
    ]
