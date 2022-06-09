# Generated by Django 4.0.4 on 2022-06-08 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reseller_portal', '0002_alter_reseller_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='reseller',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reseller',
            name='referrer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]