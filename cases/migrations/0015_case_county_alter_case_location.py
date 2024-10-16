# Generated by Django 5.1.1 on 2024-10-11 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0014_case_court_file_number_case_sub_county_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='county',
            field=models.CharField(choices=[('mombasa', 'Mombasa'), ('kwale', 'Kwale'), ('kilifi', 'Kilifi'), ('tana_river', 'Tana River'), ('lamu', 'Lamu'), ('taita_taveta', 'Taita-Taveta')], default='mombasa', max_length=100),
        ),
        migrations.AlterField(
            model_name='case',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
