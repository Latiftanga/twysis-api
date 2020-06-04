# Generated by Django 3.1a1 on 2020-06-03 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('motto', models.CharField(blank=True, max_length=255)),
                ('code', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('postal_code', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.school'),
        ),
    ]
