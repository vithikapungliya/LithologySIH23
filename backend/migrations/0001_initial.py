# Generated by Django 4.1.6 on 2023-12-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Composition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=100)),
                ("limestone_percentage", models.FloatField()),
                ("sandstone_percentage", models.FloatField()),
                ("shale_percentage", models.FloatField()),
                ("unknown_percentage", models.FloatField()),
                ("name", models.CharField(max_length=100)),
            ],
        ),
    ]
