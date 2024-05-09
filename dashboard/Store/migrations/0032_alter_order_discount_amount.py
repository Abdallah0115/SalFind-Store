# Generated by Django 4.2.5 on 2024-05-09 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0031_order_discout_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
