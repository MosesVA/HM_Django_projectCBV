# Generated by Django 5.0.9 on 2024-11-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0006_parent_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]