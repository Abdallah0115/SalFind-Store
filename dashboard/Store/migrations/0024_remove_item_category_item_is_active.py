# Generated by Django 4.2.5 on 2024-04-15 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0023_category_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.AddField(
            model_name='item',
            name='is_Active',
            field=models.BooleanField(default=True),
        ),
    ]
