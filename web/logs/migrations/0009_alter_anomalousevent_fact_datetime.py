# Generated by Django 5.0.2 on 2024-05-09 06:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0008_alter_anomalousevent_options_alter_logtype_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anomalousevent",
            name="fact_datetime",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Фактическое дата и время"
            ),
        ),
    ]