# Generated by Django 2.2.6 on 2019-10-24 12:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0003_auto_20191024_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
    ]
