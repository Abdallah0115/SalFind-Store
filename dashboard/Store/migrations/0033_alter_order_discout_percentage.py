# Generated by Django 4.2.5 on 2024-05-09 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0032_alter_order_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discout_percentage',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10, null=True),
        ),
    ]
