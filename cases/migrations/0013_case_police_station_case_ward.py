# Generated by Django 5.0.7 on 2024-10-04 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0012_alter_case_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='police_station',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='ward',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
