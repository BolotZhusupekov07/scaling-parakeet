# Generated by Django 3.2.4 on 2021-07-17 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promocode",
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
                ("name", models.CharField(max_length=500, unique=True)),
                ("discount", models.IntegerField()),
            ],
        ),
    ]
