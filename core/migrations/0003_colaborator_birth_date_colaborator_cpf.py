# Generated by Django 5.0.6 on 2024-07-06 08:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_people_colaborator'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborator',
            name='birth_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='colaborator',
            name='cpf',
            field=models.CharField(default=0, max_length=11, unique=True),
        ),
    ]
