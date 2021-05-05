# Generated by Django 3.0.5 on 2021-05-05 05:57

import apps.entry.models
import django.contrib.postgres.fields
from django.db import migrations
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0009_extractionquery_filter_figure_geographical_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionquery',
            name='filter_entry_review_status',
            field=django.contrib.postgres.fields.ArrayField(base_field=django_enumfield.db.fields.EnumField(enum=apps.entry.models.EntryReviewer.REVIEW_STATUS), blank=True, null=True, size=None),
        ),
    ]
