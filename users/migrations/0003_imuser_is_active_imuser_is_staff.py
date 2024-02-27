# Generated by Django 5.0.2 on 2024-02-27 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_imuser_is_active_remove_imuser_is_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="imuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="imuser",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]