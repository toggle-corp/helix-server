# Generated by Django 3.0.5 on 2020-08-24 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crisis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crisis',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='crisis',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_crisis', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='crisis',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By'),
        ),
        migrations.AddField(
            model_name='crisis',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified At'),
        ),
        migrations.AddField(
            model_name='crisis',
            name='version_id',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Version'),
        ),
    ]
