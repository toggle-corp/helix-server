# Generated by Django 3.0.5 on 2020-11-11 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20201102_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Phone'),
        ),
    ]