# Generated by Django 3.0.5 on 2020-11-11 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0009_auto_20201111_0707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='methodology',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='source_breakdown',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='source_methodology',
        ),
        migrations.AddField(
            model_name='entry',
            name='calculation_logic',
            field=models.TextField(blank=True, null=True, verbose_name='Calculation Logic'),
        ),
        migrations.AddField(
            model_name='entry',
            name='caveats',
            field=models.TextField(blank=True, null=True, verbose_name='Caveats'),
        ),
        migrations.AddField(
            model_name='entry',
            name='confidential',
            field=models.BooleanField(default=False, verbose_name='Confidential Source'),
        ),
    ]
