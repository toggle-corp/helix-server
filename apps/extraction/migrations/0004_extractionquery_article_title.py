# Generated by Django 3.0.5 on 2021-01-15 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extraction', '0003_extractionquery_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionquery',
            name='article_title',
            field=models.TextField(blank=True, null=True, verbose_name='Article Title'),
        ),
    ]
