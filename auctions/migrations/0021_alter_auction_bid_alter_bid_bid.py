# Generated by Django 4.2.7 on 2024-01-18 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auction_start_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
