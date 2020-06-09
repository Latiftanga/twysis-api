# Generated by Django 3.1a1 on 2020-06-09 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200603_1750'),
        ('students', '0009_auto_20200609_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.school'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='clas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='students.class'),
        ),
    ]
