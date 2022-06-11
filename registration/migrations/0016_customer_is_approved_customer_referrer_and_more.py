# Generated by Django 4.0.4 on 2022-06-09 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0015_alter_resetpasswordotp_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='referrer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resetpasswordotp',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='addresses',
            field=models.ManyToManyField(blank=True, to='registration.customeraddress'),
        ),
    ]