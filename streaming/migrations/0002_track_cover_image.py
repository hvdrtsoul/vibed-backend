# Generated by Django 4.2.20 on 2025-05-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("streaming", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="track",
            name="cover_image",
            field=models.ImageField(blank=True, null=True, upload_to="covers/"),
        ),
    ]
