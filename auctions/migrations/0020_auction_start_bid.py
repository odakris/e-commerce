# Generated by Django 4.2.7 on 2024-01-18 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_bid_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='start_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]