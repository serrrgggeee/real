# Generated by Django 2.1 on 2019-05-02 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_real', '0005_flat_izn_ztd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='izn_ztd',
        ),
    ]