# Generated by Django 3.0.5 on 2021-02-09 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0033_auto_20210204_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='figure',
            name='was_subfact',
            field=models.BooleanField(default=False),
        ),
    ]