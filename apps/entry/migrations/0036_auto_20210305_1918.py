# Generated by Django 3.0.5 on 2021-03-05 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0035_auto_20210222_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='figure',
            old_name='age_json',
            new_name='disaggregation_age_json',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='conflict',
            new_name='disaggregation_conflict',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='conflict_communal',
            new_name='disaggregation_conflict_communal',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='conflict_criminal',
            new_name='disaggregation_conflict_criminal',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='conflict_other',
            new_name='disaggregation_conflict_other',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='conflict_political',
            new_name='disaggregation_conflict_political',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='displacement_rural',
            new_name='disaggregation_displacement_rural',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='displacement_urban',
            new_name='disaggregation_displacement_urban',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='location_camp',
            new_name='disaggregation_location_camp',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='location_non_camp',
            new_name='disaggregation_location_non_camp',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='sex_female',
            new_name='disaggregation_sex_female',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='sex_male',
            new_name='disaggregation_sex_male',
        ),
        migrations.RenameField(
            model_name='figure',
            old_name='strata_json',
            new_name='disaggregation_strata_json',
        ),
    ]
