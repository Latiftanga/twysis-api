# Generated by Django 3.1a1 on 2020-06-03 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200603_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('short_name', models.CharField(max_length=10)),
                ('code', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='school',
            name='programmes',
            field=models.ManyToManyField(blank=True, null=True, related_name='schools', to='core.Programme'),
        ),
    ]
