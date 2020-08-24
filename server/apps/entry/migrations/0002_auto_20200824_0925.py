# Generated by Django 3.0.5 on 2020-08-24 09:25

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='reviewers',
            field=models.ManyToManyField(blank=True, related_name='review_entries', to=settings.AUTH_USER_MODEL, verbose_name='Reviewers'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='source_breakdown',
            field=models.TextField(blank=True, null=True, verbose_name='Source Breakdown and Reliability'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32, verbose_name='Tag'), blank=True, size=None),
        ),
    ]
