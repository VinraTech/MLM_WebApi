# Generated by Django 4.0.4 on 2022-06-14 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0021_remove_customer_city_remove_customer_referrer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='nric_no',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]