# Generated by Django 5.0.2 on 2024-05-12 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0014_remove_anomalousevent_detected_search_pattern"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationtype",
            name="method",
            field=models.CharField(
                max_length=64, unique=True, verbose_name="Метод оповещения"
            ),
        ),
    ]
