# Generated by Django 3.0.5 on 2021-01-05 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0006_householdsize'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='householdsize',
            unique_together={('country', 'year')},
        ),
    ]
