# Generated by Django 4.2.4 on 2023-08-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_app', '0008_alter_roomtype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='bathrooms',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='bedrooms',
            field=models.CharField(blank=True, null=True),
        ),
    ]
