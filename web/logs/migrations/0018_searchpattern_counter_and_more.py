# Generated by Django 5.0.2 on 2024-05-17 17:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0017_searchpattern_count_of_events_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchpattern",
            name="counter",
            field=models.BooleanField(
                default=False, verbose_name="Повторяющееся событие"
            ),
        ),
        migrations.AlterField(
            model_name="searchpattern",
            name="search_type",
            field=models.CharField(
                choices=[
                    ("SIMPLE", "По полному вхождению"),
                    ("REGEX", "Регулярное выражение"),
                    ("COEFFICIENT", "Словарный коэффициент вхождения"),
                ],
                max_length=255,
                verbose_name="Тип поиска",
            ),
        ),
    ]
