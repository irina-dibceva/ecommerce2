# Generated by Django 2.2.6 on 2019-10-28 08:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('carts', '0002_auto_20191024_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'),
                                                     ('refunded', 'Refunded')], default='created', max_length=120)),
                ('shipping_total_price', models.DecimalField(decimal_places=2, default=5.99, max_digits=50)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=50)),
                ('order_id', models.CharField(blank=True, max_length=20, null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]