# Generated by Django 5.0.2 on 2024-05-16 10:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0015_alter_notificationtype_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchpattern",
            name="coefficient",
            field=models.FloatField(
                default=None,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1),
                ],
                verbose_name="Словарный коэффициент вхождения",
            ),
        ),
    ]
