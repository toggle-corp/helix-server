# Generated by Django 3.0.5 on 2020-11-30 04:00

import apps.review.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_enumfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entry', '0016_auto_20201123_1143'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('version_id', models.CharField(blank=True, max_length=16, null=True, verbose_name='Version')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_reviewcomment', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to='entry.Entry', verbose_name='Entry')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
                ('version_id', models.CharField(blank=True, max_length=16, null=True, verbose_name='Version')),
                ('field', models.CharField(max_length=256, verbose_name='Field')),
                ('value', django_enumfield.db.fields.EnumField(enum=apps.review.models.Review.REVIEW_STATUS)),
                ('age_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='Age ID')),
                ('strata_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='Strata ID')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='review.ReviewComment', verbose_name='Comment')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_review', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='entry.Entry', verbose_name='Entry')),
                ('figure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='figure_reviews', to='entry.Figure', verbose_name='Figure')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
