# Generated by Django 2.1 on 2019-05-02 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_real', '0003_auto_20190502_0505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='net_sale2',
        ),
    ]
