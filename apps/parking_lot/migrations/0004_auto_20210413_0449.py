# Generated by Django 3.0.5 on 2021-04-13 04:49

import apps.parking_lot.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('parking_lot', '0003_auto_20210127_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkeditem',
            name='meta_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='parkeditem',
            name='source',
            field=django_enumfield.db.fields.EnumField(blank=True, enum=apps.parking_lot.models.ParkedItem.PARKING_LOT_SOURCE, null=True),
        ),
        migrations.AddField(
            model_name='parkeditem',
            name='source_uuid',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Source Uuid'),
        ),
    ]