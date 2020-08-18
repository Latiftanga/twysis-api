# Generated by Django 3.1 on 2020-08-14 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_house'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=32)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=32)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='core.school')),
            ],
        ),
    ]
