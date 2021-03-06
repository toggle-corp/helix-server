# Generated by Django 3.0.5 on 2021-02-05 11:11

import apps.crisis.models
from django.db import migrations, models
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0032_merge_20210203_0407'),
        ('crisis', '0003_auto_20210127_0845'),
        ('country', '0008_auto_20210202_0517'),
        ('extraction', '0005_merge_20210125_0524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extractionquery',
            old_name='article_title',
            new_name='entry_article_title',
        ),
        migrations.RenameField(
            model_name='extractionquery',
            old_name='event_before',
            new_name='figure_end_before',
        ),
        migrations.RenameField(
            model_name='extractionquery',
            old_name='event_after',
            new_name='figure_start_after',
        ),
        migrations.RemoveField(
            model_name='extractionquery',
            name='countries',
        ),
        migrations.RemoveField(
            model_name='extractionquery',
            name='crises',
        ),
        migrations.RemoveField(
            model_name='extractionquery',
            name='figure_tags',
        ),
        migrations.RemoveField(
            model_name='extractionquery',
            name='regions',
        ),
        migrations.AddField(
            model_name='extractionquery',
            name='entry_tags',
            field=models.ManyToManyField(blank=True, related_name='_extractionquery_entry_tags_+', to='entry.FigureTag', verbose_name='Figure Tags'),
        ),
        migrations.AddField(
            model_name='extractionquery',
            name='event_countries',
            field=models.ManyToManyField(blank=True, related_name='_extractionquery_event_countries_+', to='country.Country', verbose_name='Countries'),
        ),
        migrations.AddField(
            model_name='extractionquery',
            name='event_crises',
            field=models.ManyToManyField(blank=True, related_name='_extractionquery_event_crises_+', to='crisis.Crisis', verbose_name='Crises'),
        ),
        migrations.AddField(
            model_name='extractionquery',
            name='event_crisis_type',
            field=django_enumfield.db.fields.EnumField(blank=True, enum=apps.crisis.models.Crisis.CRISIS_TYPE, null=True),
        ),
        migrations.AddField(
            model_name='extractionquery',
            name='event_regions',
            field=models.ManyToManyField(blank=True, related_name='_extractionquery_event_regions_+', to='country.CountryRegion', verbose_name='Regions'),
        ),
    ]
