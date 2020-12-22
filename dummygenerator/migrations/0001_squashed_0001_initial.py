# Generated by Django 2.2.17 on 2020-12-22 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('dummygenerator', '0001_initial')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FakeCSVSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('column_separator', models.CharField(choices=[(',', 'Comma (,)'), (';', 'Semicolon (;)'), ('\t', 'Tab (\t)'), (' ', 'Space ( )'), ('|', 'Vertical bar (|)')], default=',', max_length=1)),
                ('string_character', models.CharField(choices=[('"', 'Double-quote (")'), ("'", "Single-quote (')")], default='"', max_length=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userschemas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FakeCSVSchemaColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='column name')),
                ('data_type', models.IntegerField(choices=[(0, 'Full name (a combination of first name and last name)'), (1, 'Job'), (2, 'Email'), (3, 'Domain name'), (4, 'Phone number'), (5, 'Company name'), (6, 'Text (with specified range for a number of sentences)'), (7, 'Integer (with specified range)'), (8, 'Address'), (9, 'Date')], verbose_name='type')),
                ('order', models.IntegerField(blank=True, default=0)),
                ('data_range_from', models.IntegerField(blank=True, null=True)),
                ('data_range_to', models.IntegerField(blank=True, null=True)),
                ('target_schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemacolumns', to='dummygenerator.FakeCSVSchema')),
            ],
        ),
    ]
