# Generated by Django 4.0.4 on 2022-06-04 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_website', '0003_cart_productcolors_productimages_productreview_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.ImageField(upload_to='images/products/'),
        ),
    ]
