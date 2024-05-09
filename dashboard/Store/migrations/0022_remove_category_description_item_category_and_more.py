# Generated by Django 4.2.5 on 2024-04-14 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0021_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AddField(
            model_name='item',
            name='Category',
            field=models.ForeignKey(default='Others', on_delete=django.db.models.deletion.CASCADE, to='Store.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(default='good item with good price you can order it any time from our store have amazing ablities', max_length=1000),
        ),
    ]
