# Generated by Django 4.2.5 on 2024-04-14 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0022_remove_category_description_item_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default='good category with good prices you can order it any time from our store have amazing ablities', max_length=500),
        ),
    ]
