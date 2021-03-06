# Generated by Django 3.0.5 on 2020-11-19 08:58

from django.db import migrations


def create_through_relations(apps, schema_editor):
    Entry = apps.get_model('entry', 'Entry')
    EntryReviewer = apps.get_model('entry', 'EntryReviewer')
    for entry in Entry.objects.all():
        for reviewer in entry.reviewers.all():
            EntryReviewer(
                entry=entry,
                reviewer=reviewer,
                status=None
            ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0012_entryreviewer'),
    ]

    operations = [
        migrations.RunPython(create_through_relations, reverse_code=migrations.RunPython.noop),
    ]
