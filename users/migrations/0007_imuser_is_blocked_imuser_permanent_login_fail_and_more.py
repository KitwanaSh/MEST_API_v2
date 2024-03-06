# Generated by Django 5.0.2 on 2024-03-06 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_cohort_cohortmember"),
    ]

    operations = [
        migrations.AddField(
            model_name="imuser",
            name="is_blocked",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="imuser",
            name="permanent_login_fail",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="imuser",
            name="temporal_login_fail",
            field=models.IntegerField(default=0),
        ),
    ]
