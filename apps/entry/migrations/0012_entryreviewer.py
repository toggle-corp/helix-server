# Generated by Django 3.0.5 on 2020-11-19 08:56

import apps.entry.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entry', '0011_auto_20201112_0504'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryReviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_enumfield.db.fields.EnumField(blank=True, enum=apps.entry.models.EntryReviewer.REVIEW_STATUS, null=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewing', to='entry.Entry', verbose_name='Entry')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewing', to=settings.AUTH_USER_MODEL, verbose_name='Reviewer')),
            ],
        ),
    ]
