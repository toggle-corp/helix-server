# Generated by Django 3.0.5 on 2020-11-23 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0015_entry_reviewers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'permissions': (('sign_off_entry', 'Can sign off the entry'),)},
        ),
    ]
