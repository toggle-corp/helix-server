# Generated by Django 3.0.5 on 2020-12-10 04:38

import apps.entry.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_organization_deleted_on'),
        ('entry', '0016_auto_20201123_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='OSMName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('wikipedia', models.TextField(blank=True, null=True, verbose_name='Wikipedia')),
                ('rank', models.IntegerField(blank=True, null=True, verbose_name='Rank')),
                ('country', models.TextField(verbose_name='Country')),
                ('country_code', models.CharField(max_length=8, verbose_name='Country Code')),
                ('street', models.TextField(blank=True, null=True, verbose_name='Street')),
                ('wiki_data', models.TextField(blank=True, null=True, verbose_name='Wiki data')),
                ('osm_id', models.CharField(max_length=256, verbose_name='OSM Id')),
                ('osm_type', models.CharField(max_length=256, verbose_name='OSM Type')),
                ('house_numbers', models.TextField(blank=True, null=True, verbose_name='House numbers')),
                ('identifier', models.IntegerField(verbose_name='Identifier')),
                ('city', models.CharField(blank=True, max_length=256, null=True, verbose_name='City')),
                ('display_name', models.CharField(max_length=512, verbose_name='Display name')),
                ('lon', models.FloatField(verbose_name='Longitude')),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('state', models.TextField(blank=True, null=True, verbose_name='State')),
                ('bounding_box', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None, verbose_name='Bounding Box')),
                ('type', models.TextField(blank=True, null=True, verbose_name='Type')),
                ('importance', models.FloatField(blank=True, null=True, verbose_name='Importance')),
                ('class_name', models.TextField(blank=True, null=True, verbose_name='Class')),
                ('name', models.TextField(verbose_name='Name')),
                ('name_suffix', models.TextField(blank=True, null=True, verbose_name='Name Suffix')),
                ('place_rank', models.IntegerField(blank=True, null=True, verbose_name='Place Rank')),
                ('alternative_names', models.TextField(blank=True, null=True, verbose_name='Alternative names')),
                ('accuracy', django_enumfield.db.fields.EnumField(enum=apps.entry.models.OSMName.OSM_ACCURACY)),
                ('reported_name', models.TextField(verbose_name='Reported Name')),
                ('moved', models.BooleanField(default=False, verbose_name='Moved')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='entry',
            name='preview',
            field=models.OneToOneField(blank=True, help_text='After the preview has been generated pass its idalong during entry creation, so that during entry update the preview can be obtained.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entry', to='entry.SourcePreview'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='published_entries', to='organization.Organization', verbose_name='Publisher'),
        ),
        migrations.AddField(
            model_name='figure',
            name='destinations',
            field=models.ManyToManyField(related_name='_figure_destinations_+', to='entry.OSMName', verbose_name='Destination'),
        ),
        migrations.AddField(
            model_name='figure',
            name='sources',
            field=models.ManyToManyField(related_name='_figure_sources_+', to='entry.OSMName', verbose_name='Source'),
        ),
    ]
