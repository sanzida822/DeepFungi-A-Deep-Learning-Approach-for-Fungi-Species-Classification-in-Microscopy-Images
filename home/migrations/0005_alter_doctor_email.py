# Generated by Django 5.0.7 on 2024-08-12 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_hospital_doctor_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
