# Generated by Django 5.0.9 on 2024-11-03 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0005_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is_active'),
        ),
    ]