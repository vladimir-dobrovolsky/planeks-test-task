# Generated by Django 2.2.17 on 2020-12-20 14:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("dummygenerator", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fakecsvschema",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fakecsvschema",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
