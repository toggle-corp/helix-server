# Generated by Django 3.0.5 on 2021-03-31 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0040_merge_20210330_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='figure',
            name='is_housing_destruction',
            field=models.BooleanField(blank=True, null=True, verbose_name='Housing destruction (recommended estimate for this entry)'),
        ),
    ]
