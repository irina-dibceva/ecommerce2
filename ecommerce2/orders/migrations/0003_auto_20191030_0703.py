# Generated by Django 2.2.6 on 2019-10-30 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('billing', '0001_initial'),
        ('orders', '0002_auto_20191028_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='billing.BillingProfile'),
        ),
    ]