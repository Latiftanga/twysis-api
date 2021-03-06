# Generated by Django 3.1a1 on 2020-06-07 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200603_1750'),
        ('students', '0006_auto_20200607_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('status', models.CharField(choices=[('Boarding', 'Boarding'), ('Day', 'Day')], max_length=40)),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(max_length=255)),
                ('residential_address', models.CharField(max_length=255)),
                ('hometown', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('clas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='students.class')),
                ('guardians', models.ManyToManyField(blank=True, related_name='students', to='students.Guardian')),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='students.house')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
    ]
