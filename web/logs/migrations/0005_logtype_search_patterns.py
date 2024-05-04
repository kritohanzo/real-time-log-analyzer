# Generated by Django 5.0.2 on 2024-05-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logs", "0004_alter_logtype_options_remove_searchpattern_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="logtype",
            name="search_patterns",
            field=models.ManyToManyField(
                related_name="log_types",
                through="logs.LogTypeSearchPattern",
                to="logs.searchpattern",
                verbose_name="Поисковые паттерны",
            ),
        ),
    ]
