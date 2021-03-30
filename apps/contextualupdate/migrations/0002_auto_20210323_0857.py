# Generated by Django 3.0.5 on 2021-03-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contextualupdate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contextualupdate',
            name='caveats',
            field=models.TextField(blank=True, null=True, verbose_name='Caveats'),
        ),
        migrations.AddField(
            model_name='contextualupdate',
            name='excerpt_idu',
            field=models.TextField(blank=True, null=True, verbose_name='Excerpt for IDU'),
        ),
    ]