# Generated by Django 4.2.5 on 2024-04-03 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_remove_cust_groups_cust_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cust',
            name='cust_id',
        ),
    ]
