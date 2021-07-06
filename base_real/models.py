from django.db import models
from django.contrib.postgres.validators import RangeMinValueValidator
from django.contrib.postgres.fields import IntegerRangeField


COUNT_ROOM = (
        (0, 'Студия'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4+'),
    )

PLANING = (
        (0, 'изолированная'),
        (1, 'свободная'),
        (2, 'смежная'),
        (3, 'смежно-изолированная'),
        (4, 'другое'),
    )


class Underground(models.Model):
	name = models.CharField('Название метро', max_length=255, blank=True, null=True, default=None)
	def __str__(self):
		return self.name


class TypeObject(models.Model):
	name = models.CharField('Название типа объекта', max_length=255, blank=True, null=True, default=None)
	def __str__(self):
		return self.name


class Closet(models.Model):
	name = models.CharField('Название елементов санузла', max_length=255, blank=True, null=True, default=None)
	def __str__(self):
		return self.name


class Flat(models.Model):
	underground = models.ManyToManyField(Underground, blank=True, default=None, verbose_name='Метро')
	type_object = models.ForeignKey(TypeObject, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Вид объекта')
	total_area = IntegerRangeField('Общая площадь, м2', null=True, blank=True)
	houseroom = IntegerRangeField('Жилая площадь, м2', null=True, blank=True)
	area_kitchen = IntegerRangeField('Площадь кухни, м2', null=True, blank=True)
	material_building = models.CharField('Материал здания', max_length=255, blank=True, null=True, default=None)
	floor = IntegerRangeField('Этаж (число, от - до)', null=True, blank=True)
	not_first_floor = models.BooleanField('Не первый этаж', default=False)
	not_last_floor = models.BooleanField('Не последний этаж (чекбокс)', default=False)
	count_floor = IntegerRangeField('Этажность (число, от - до)', null=True, blank=True)
	count_room = models.PositiveSmallIntegerField('Количество комнат', blank=True, choices=COUNT_ROOM, default=0)
	planing = models.PositiveSmallIntegerField('Планировка', blank=True, choices=PLANING, default=0)
	closet = models.ManyToManyField(Closet, blank=True, default=None, verbose_name='Санузел')
	balcony = models.BooleanField('Балкон', default=False)
	loggia = models.BooleanField('Лоджия', default=False)
	with_photo = models.BooleanField('С фотографией', default=False)
	hypothec = models.BooleanField('Ипотека', default=False)
	bargain = models.BooleanField('Торг', default=False)
	exchange = models.BooleanField('Обмен', default=False)
	net_sale = models.BooleanField('Чистая продажа', default=False)

	def get_mardown(self):
		return 'get_mardown'

