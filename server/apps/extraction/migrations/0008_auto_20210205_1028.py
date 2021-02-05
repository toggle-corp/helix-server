# Generated by Django 3.0.5 on 2021-02-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0032_merge_20210203_0407'),
        ('extraction', '0007_auto_20210205_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extractionquery',
            name='event_tags',
        ),
        migrations.AddField(
            model_name='extractionquery',
            name='entry_tags',
            field=models.ManyToManyField(blank=True, related_name='_extractionquery_entry_tags_+', to='entry.FigureTag', verbose_name='Figure Tags'),
        ),
    ]