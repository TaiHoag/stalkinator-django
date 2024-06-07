# Generated by Django 5.0.6 on 2024-06-07 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="geofence",
            name="categories",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="geofence",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="geofence",
            name="radius",
            field=models.IntegerField(default=1000),
        ),
    ]