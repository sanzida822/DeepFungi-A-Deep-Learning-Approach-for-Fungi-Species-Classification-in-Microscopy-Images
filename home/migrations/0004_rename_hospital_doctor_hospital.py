# Generated by Django 5.0.7 on 2024-08-12 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='Hospital',
            new_name='hospital',
        ),
    ]
