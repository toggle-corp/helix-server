# Generated by Django 3.0.5 on 2021-04-23 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0010_countrypopulation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='idmc_short_name',
            field=models.CharField(max_length=256, verbose_name='IDMC Short Name'),
        ),
    ]
