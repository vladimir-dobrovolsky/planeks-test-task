# Generated by Django 2.2.17 on 2020-12-20 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dummygenerator", "0003_auto_20201220_1925"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fakecsvschema",
            name="name",
            field=models.TextField(blank=True, null=True),
        ),
    ]
