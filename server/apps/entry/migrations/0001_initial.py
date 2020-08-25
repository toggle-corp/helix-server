# Generated by Django 3.0.5 on 2020-08-24 07:05

import apps.entry.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0001_squashed_0003_auto_20200820_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Source URL')),
                ('article_title', models.TextField(verbose_name='Article Title')),
                ('source', models.CharField(max_length=256, verbose_name='Source')),
                ('publisher', models.CharField(max_length=256, verbose_name='Publisher')),
                ('publish_date', models.DateField(verbose_name='Published Date')),
                ('source_methodology', models.TextField(blank=True, null=True, verbose_name='Source Methodology')),
                ('source_excerpt', models.TextField(blank=True, null=True, verbose_name='Excerpt from Source')),
                ('source_breakdown', models.TextField(verbose_name='Source Breakdown and Reliability')),
                ('idmc_analysis', models.TextField(null=True, verbose_name='IDMC Analysis')),
                ('methodology', models.TextField(null=True, verbose_name='Methodology')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32, verbose_name='Tag'), size=None)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='event.Event', verbose_name='Event')),
                ('reviewers', models.ManyToManyField(related_name='review_entries', to=settings.AUTH_USER_MODEL, verbose_name='Reviewers')),
            ],
        ),
        migrations.CreateModel(
            name='Figure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.TextField(verbose_name='District(s)')),
                ('town', models.CharField(max_length=256, verbose_name='Town/Village')),
                ('quantifier', django_enumfield.db.fields.EnumField(enum=apps.entry.models.Figure.QUANTIFIER)),
                ('reported', models.PositiveIntegerField(verbose_name='Reported Figures')),
                ('unit', django_enumfield.db.fields.EnumField(default=0, enum=apps.entry.models.Figure.UNIT)),
                ('term', django_enumfield.db.fields.EnumField(default=0, enum=apps.entry.models.Figure.TERM)),
                ('type', django_enumfield.db.fields.EnumField(default=0, enum=apps.entry.models.Figure.TYPE)),
                ('role', django_enumfield.db.fields.EnumField(default=0, enum=apps.entry.models.Figure.ROLE)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('include_idu', models.BooleanField(verbose_name='Include in IDU')),
                ('excerpt_idu', models.TextField(verbose_name='Excerpt for IDU')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='figures', to='entry.Entry', verbose_name='Entry')),
            ],
        ),
    ]