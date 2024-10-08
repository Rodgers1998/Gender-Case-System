# Generated by Django 5.0.7 on 2024-08-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0007_alter_case_case_type_alter_case_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_type',
            field=models.CharField(choices=[('abduction', 'Abduction'), ('defilement', 'Defilement'), ('neglegence', 'Neglegence'), ('legal councelling', 'Legal Councelling'), ('emotional abuse', 'Emotional Abuse'), ('child abuse', 'Child Abuse'), ('physical assault', 'Physical Assault'), ('domestic violence', 'Violence'), ('attempted defilement', 'Attempted Defilement'), ('sodomy', 'Sodomy'), ('rape', 'Rape'), ('juvenile deliquency', 'Juvenile Deliquency'), ('attempted sodomy', 'Attempted Sodomy'), ('attempted rape', 'Attempted Rape'), ('sexual assault', 'Sexual Assault'), ('indicent act', 'Incident Act'), ('sexual harrassment', 'Sexual Harrassment')], max_length=100),
        ),
        migrations.AlterField(
            model_name='case',
            name='location',
            field=models.CharField(choices=[('runyu', 'Runyu'), ('miritini', 'Miritini'), ('birikani', 'Birikani'), ('giriamani', 'Giriamani'), ('nairobi area', 'Nairobi Area'), ('centre', 'Centre'), ('mkupe', 'Mkupe'), ('kachimbeni', 'Kachimbani'), ('darajani', 'Darajani'), ('majengo', 'Majengo'), ('kibarani', 'Kibirani'), ('kwashee', 'Kwashee'), ('ganahola', 'Ganahola'), ('aldina', 'Aldina'), ('owino huru', 'Owino Huru'), ('chamunyu jomvu', 'Chamunyu Jomvu'), ('staff', 'Staff'), ('jomvu', 'Jomvu'), ('majengo mapya', 'Majengo Mapya'), ('kwa mwanzia', 'Kwa Mwanzia'), ('kilifi south', 'Kilifi South'), ('likoni', 'Likoni'), ('kisauni', 'Kisauni'), ('nyali', 'Nyali'), ('changamwe', 'Changamwe'), ('kwapunda', 'Kwapunda'), ('bahati', 'Bahati')], max_length=255),
        ),
    ]
