# Generated by Django 5.0.2 on 2024-05-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0020_alter_anomalousevent_count_of_events"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anomalousevent",
            name="text",
            field=models.CharField(max_length=2048, verbose_name="Текст"),
        ),
    ]
