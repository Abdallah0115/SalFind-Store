# Generated by Django 4.2.5 on 2024-04-13 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_item_discav'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='month',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ref_num',
        ),
        migrations.RemoveField(
            model_name='order',
            name='year',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
