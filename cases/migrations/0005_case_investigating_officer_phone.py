# Generated by Django 5.0.7 on 2024-08-20 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0004_alter_case_accused_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='investigating_officer_phone',
            field=models.CharField(default='000-000-0000', max_length=15),
        ),
    ]
