# Generated by Django 4.0.4 on 2022-06-13 19:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0019_customer_referrer_id_customer_referrer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 6, 14, 1, 6, 0, 64520)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2022, 6, 14, 1, 6, 10, 760206)),
            preserve_default=False,
        ),
    ]
