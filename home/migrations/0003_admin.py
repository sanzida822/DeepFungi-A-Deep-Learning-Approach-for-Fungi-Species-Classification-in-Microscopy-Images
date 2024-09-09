# Generated by Django 5.0.7 on 2024-08-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_doctor_delete_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50, verbose_name='Password')),
            ],
        ),
    ]
