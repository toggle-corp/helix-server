# Generated by Django 3.0.5 on 2020-12-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0002_auto_20201105_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='iso2',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='ISO2'),
        ),
    ]