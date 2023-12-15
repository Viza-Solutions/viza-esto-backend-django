# Generated by Django 4.2.3 on 2023-08-02 22:21

from django.db import migrations, models
import tenant_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_app', '0003_tenant_date_of_birth_tenant_date_of_lease_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='agent_commission',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='agent_id_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='agent_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='agent_phone',
            field=tenant_app.models.KenyanPhoneNumberField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='agent_trasaction_ref',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='intro_by',
            field=models.CharField(choices=[('Self', 'Self'), ('Agent', 'Agent')], default='Self', max_length=5),
        ),
    ]
