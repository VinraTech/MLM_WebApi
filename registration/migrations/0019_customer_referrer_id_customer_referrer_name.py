# Generated by Django 4.0.4 on 2022-06-13 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0018_customer_created_at_customer_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='referrer_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='referrer_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]