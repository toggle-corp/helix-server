# Generated by Django 3.0.5 on 2021-01-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0002_auto_20210106_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionquery',
            name='name',
            field=models.CharField(default='default', max_length=128, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
