# Generated by Django 4.0.4 on 2022-06-02 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.PositiveBigIntegerField(),
        ),
    ]