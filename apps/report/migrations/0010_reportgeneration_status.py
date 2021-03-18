# Generated by Django 3.0.5 on 2021-03-12 07:07

import apps.report.models
from django.db import migrations
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0009_auto_20210305_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportgeneration',
            name='status',
            field=django_enumfield.db.fields.EnumField(enum=apps.report.models.ReportGeneration.REPORT_GENERATION_STATUS, null=True),
        ),
    ]
