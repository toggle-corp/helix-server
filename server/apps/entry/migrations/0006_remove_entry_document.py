# Generated by Django 3.0.5 on 2020-11-05 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0005_remove_sourcepreview_pdf_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='document',
        ),
    ]
