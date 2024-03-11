# Generated by Django 5.0.2 on 2024-03-10 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0003_alter_anomalouslogevent_datetime"),
    ]

    operations = [
        migrations.AddField(
            model_name="logfile",
            name="last_positions",
            field=models.IntegerField(
                default=0, verbose_name="Последняя позиция при чтении"
            ),
        ),
        migrations.AlterField(
            model_name="anomalouslogevent",
            name="datetime",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 10, 9, 15, 43, 141593, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата и время события лог-файла",
            ),
        ),
    ]