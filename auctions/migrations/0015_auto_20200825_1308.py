# Generated by Django 3.1 on 2020-08-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20200825_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='your_bids',
            field=models.FloatField(default=0),
        ),
    ]