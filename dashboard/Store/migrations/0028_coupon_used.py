# Generated by Django 4.2.5 on 2024-04-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0027_coupon_cust_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='used',
            field=models.BooleanField(default=True),
        ),
    ]
