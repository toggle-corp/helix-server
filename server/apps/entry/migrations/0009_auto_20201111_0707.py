# Generated by Django 3.0.5 on 2020-11-11 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20201109_0758'),
        ('entry', '0008_auto_20201111_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_entires', to='organization.Organization', verbose_name='Publisher'),
        ),
        migrations.AddField(
            model_name='entry',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sourced_entries', to='organization.Organization', verbose_name='Source'),
        ),
    ]