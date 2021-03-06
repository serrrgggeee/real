# Generated by Django 2.1 on 2018-08-06 18:21

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Closet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Название елементов санузла')),
            ],
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_area', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, null=True, verbose_name='Общая площадь, м2')),
                ('houseroom', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, null=True, verbose_name='Жилая площадь, м2')),
                ('area_kitchen', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, null=True, verbose_name='Площадь кухни, м2')),
                ('material_building', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Материал здания')),
                ('floor', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, null=True, verbose_name='Этаж (число, от - до)')),
                ('not_first_floor', models.BooleanField(default=False, verbose_name='Не первый этаж')),
                ('not_last_floor', models.BooleanField(default=False, verbose_name='Не последний этаж (чекбокс)')),
                ('count_floor', django.contrib.postgres.fields.ranges.IntegerRangeField(blank=True, null=True, verbose_name='Этажность (число, от - до)')),
                ('count_room', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Студия'), (1, '1'), (2, '2'), (3, '3'), (4, '4+')], default=0, verbose_name='Количество комнат')),
                ('planing', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'изолированная'), (1, 'свободная'), (2, 'смежная'), (3, 'смежно-изолированная'), (4, 'другое')], default=0, verbose_name='Планировка')),
                ('balcony', models.BooleanField(default=False, verbose_name='Балкон')),
                ('loggia', models.BooleanField(default=False, verbose_name='Лоджия')),
                ('with_photo', models.BooleanField(default=False, verbose_name='С фотографией')),
                ('hypothec', models.BooleanField(default=False, verbose_name='Ипотека')),
                ('bargain', models.BooleanField(default=False, verbose_name='Торг')),
                ('exchange', models.BooleanField(default=False, verbose_name='Обмен')),
                ('net_sale', models.BooleanField(default=False, verbose_name='Чистая продажа')),
                ('closet', models.ManyToManyField(blank=True, default=None, to='base_real.Closet', verbose_name='Санузел')),
            ],
        ),
        migrations.CreateModel(
            name='TypeObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Название типа объекта')),
            ],
        ),
        migrations.CreateModel(
            name='Underground',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Название метро')),
            ],
        ),
        migrations.AddField(
            model_name='flat',
            name='type_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base_real.TypeObject', verbose_name='Вид объекта'),
        ),
        migrations.AddField(
            model_name='flat',
            name='underground',
            field=models.ManyToManyField(blank=True, default=None, to='base_real.Underground', verbose_name='Метро'),
        ),
    ]
