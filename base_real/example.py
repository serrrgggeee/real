# first example

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


class MixinSerializer(Serializer):
	total_area = SerializerMethodField()
	houseroom = SerializerMethodField()
	area_kitchen = SerializerMethodField()
	floor = SerializerMethodField()
	count_floor = SerializerMethodField()
	url = HyperlinkedIdentityField(
		view_name=(__package__)+'-api:detail',
		lookup_field='pk'
		)
	delete_url = HyperlinkedIdentityField(
		view_name=(__package__)+'-api:delete',
		lookup_field='pk'
		)

	def get_total_area(self, obj):
		area = {}
		if obj.total_area:
			area.update({'lower': obj.total_area.lower})
			area.update({'upper': obj.total_area.upper})

		return area

	def get_houseroom(self, obj):
		room = {}
		if obj.houseroom:
			room.update({'lower': obj.houseroom.lower})
			room.update({'upper': obj.houseroom.upper})
		return room

	def get_area_kitchen(self, obj):
		area_kitchen = {}
		if obj.area_kitchen:
			area_kitchen.update({'lower': obj.area_kitchen.lower})
			area_kitchen.update({'upper': obj.area_kitchen.upper})

		return area_kitchen

	def get_floor(self, obj):
		floor = {}
		if obj.floor:
			floor.update({'lower': obj.floor.lower})
			floor.update({'upper': obj.floor.upper})

		return floor

	def get_count_floor(self, obj):
		count_floor = {}
		if obj.count_floor:
			count_floor.update({'lower': obj.count_floor.lower})
			count_floor.update({'upper': obj.count_floor.upper})

		return count_floor

class CreateUpdateSerializer(ModelSerializer, MixinSerializer):
	class Meta:
		model = Flat
		fields = fields


class CreateAPIView(CreateAPIView):
	queryset = Flat.objects.all()
	serializer_class = CreateUpdateSerializer
	permission_classes = [IsAuthenticated]

	def get_serializer_context(self):
		underground = self.request.POST.get('underground')
		if underground:
			underground = json.loads(underground)
			self.un = Underground.objects.create(**underground)
		return {'request': self.request}

	def perform_create(self, serializer):
		serializer.save(underground=[self.un])

# second example
class Place(MPTTModel, ModelMeta):
    name = models.CharField('Название населенного пункта',  max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    type_place = models.CharField('Тип населенного пункта',  max_length=128)
    show = models.BooleanField(default=False,  verbose_name='Отображать на сайте')
    first_order = models.BooleanField(default=False,  verbose_name='Первые в списке')
    pub_date = models.DateTimeField('Срок размещения в днях', default=now)
    image_description = models.ImageField(upload_to='main_page', verbose_name='Image', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    seo_title = models.CharField(max_length=160, null=True, blank=True)
    seo_description = models.CharField(max_length=160, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name or self.code or ''

    def get_absolute_url(self):
        return reverse('single_place', kwargs={'id': self.pk})


class SinglePlaceView(TemplateView):
    template_name = 'place/single_place.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        data['single_place']=Place.objects.prefetch_related('photo').get(id=id, show=True)
        return data

{% extends "base.html" %}
{% load mptt_tags thumbnail%}
{% block title %}<title itemprop="name">{{single_place.seo_title|default:"Октябрьский район Волгоградская область"}}</title>{% endblock %}
{% block description %}<meta name="description" content="{{single_place.seo_description|default:"Октябрьский район Волгоградская область"}}" />{% endblock %}
{% block content %}
<div class="col-md-3 left-side">
    <div class="row place">
        <div class="col-md-12">
            <ul>
                {% recursetree categories %}

                {% if node.is_root_node %}

                <a class="underline parent" href="/{{node.id}}/">{{ node.name }}</a>
                {% endif %}
                {% if not node.is_root_node %}
                <a class="children" href="/{{node.id}}/">
                    <li class="child">{{ node.name }}</li>
                </a>
                {% endif %}
                {% if not node.is_leaf_node %}
                {{ children }}
                {% endif %}

                {% endrecursetree %}
            </ul>
        </div>
    </div>
    {% include 'includes/side_menu.html'%}

</div>
<div class="col-md-9 col-md-offset- right-side">

        <div class="row single_place">
            {% include "place/modal/context.html" %}
        </div>
</div>
{% endblock %}


# third example
class ImportExelView(TemplateView):
	template_name = 'admin/import/exelimport.html'
	form_class = ImportExelForm

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)

		if form.is_valid():
			self.get_values()
			self.set_succeess()
			return redirect('/admin/')
		else:
			self.set_not_exist('wrong')
			return redirect('/admin/')

	def _replace(text):
		return text.replace(
 			u'\xa0', '').replace(u'\xae', '').replace(u'\xe4r', '').replace(
			u'\u2122', '').replace(u'\xc0', u'A').replace(u'\u200b', '')

	def get_values_openpyxl(self, file_path):
		wb = load_workbook(file_path)

	def set_month(self):
		month = self.request.POST.get('month')
		return month if len(month) == 2 else '0'+ month

	def get_values(self):
		file = self.request.FILES.get('file').name
		self.get_header(file)
		file_path = '/tmp/{0}'.format(file)
		self.handle_uploaded_file(file_path, self.request.FILES.get('file'))
		rb = xlrd.open_workbook(file_path)
		sheet = rb.sheet_by_index(0)
		self.type_product = TypeProduct.objects.get(pk = self.type_product)
		self.save_to_product(sheet)

	def save_to_product(self, sheet):	
		for rownum in range(1, sheet.nrows):
			row = sheet.row_values(rownum)
			title = row[5] if row[5] else ''
			description = row[2] if row[2] else ''
			status = row[3] if row[3] else'ex'
			if status == 'ex' or self.store:
				price = row[1]
				defaults = {
							'status': status,
					 		'name':row[0],
					 		'title': title,
							'description':description,
							'current_price':price, 
							'type_product':self.type_product,
							'created':self.created
						}

				product, create = Product.objects.update_or_create(name=row[0], 
												shop=self.shop, city=self.city,
												defaults=defaults)
				defaults['status'] = 'noex'
				Product.objects.update_or_create(name=row[0], 
											shop=self.shop_store, city=self.city, defaults=defaults)
				defaults = {'price': price}
				Price.objects.update_or_create(shop=self.shop, created=self.created, product=product, defaults=defaults)			
				rowcat = row[4].split(',')
				for cat in rowcat:
					category, create = Category.objects.get_or_create(name=cat)
					product.categories.add(category)

	def set_not_exist(self, thing):
		messages.success(self.request, thing)
 
	def set_succeess(self):
		messages.success(self.request, 'ok')
		return redirect('/admin/')

	def get_header(self, file=None):
		relation = None
		if file:
			relation = file.split('.')[0].split('_')
		if relation:
			self.shop = self.get_shop(relation[0])

			self.store = False
			if(relation[0] == 'store'):
				self.store = True
			try:
				self.created = relation[1]
			except IndexError:
				pass
		self.shop_store = self.get_shop('store')
		self.type_product = self.request.POST.get('type_product')
		self.city = self.get_city_by_id(self.request.POST.get('city'))

	def get_city(self, sighn):
		try:
			return City.objects.get(city_sighn=sighn)
		except City.DoesNotExist:
			self.set_not_exist('sity')

	def get_city_by_id(self, id):
		try:
			return City.objects.get(pk=id)
		except City.DoesNotExist:
			self.set_not_exist('sity')

	def get_shop(self, sighn):
		try:
			return Shop.objects.get(shop_sighn=sighn)
		except Shop.DoesNotExist:
			return Shop.objects.get(pk=sighn)

	def get_type_product(self, sighn):
		try:
			return TypeProduct.objects.get(type_sighn=sighn)
		except TypeProduct.DoesNotExist:
			return TypeProduct.objects.get(pk=sighn)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		return context

	def handle_uploaded_file(self, file_path, file):
		with open(file_path, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)

	def unzip(self, source_filename):
		file_extract = '/tmp/{0}'.format(request.FILES['file'].name.split('.')[0])
		zip_ref = zipfile.ZipFile(source_filename, 'r')
		zip_ref.extractall(dest_dir)
		zip_ref.close()


class ImportLentaView(ImportExelView):
	template_name = 'admin/import/lentaimport.html'
	form_class = ImportLentaForm

	def get_values(self):
		shop_url = 'http://www.lenta.com/'
		file = self.request.POST.get('shop_type')
		date = self.request.POST.get('date')
		url_product = self.request.POST.get('url')
		url_product = Parsing.objects.get(pk=url_product).url
		self.get_header(file)
		defaults = {}
		parse = True
		url = '{0}'.format(url_product)
		category = ['косметика']
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page)
		for anchor in soup.find_all(class_='table_tr_week_list'):
			type_product = self.type_product
			product = anchor.find(class_='week_list__title')
			if product is None: continue
			description = title = name = product.get_text()
			status = 'ex'
			url_page = url_product
			price = self.getPrice(anchor)
			url_page = '{0}{1}'.format(shop_url, url_page)
			defaults = {
				'status': status,
				'name':name,
				'url': url_page,
				'title': title,
				'description':description,
				'current_price':price,
				'type_product':type_product,
				'created': date,
			}
			self.save_to_product(defaults, category)

	def getPrice(self, elm):
		try:
			str = elm.find(class_='week_list_new-price').get_text()
			str = re.sub(r'[a-zA-Zа-яА-Я_]', '', str)
			str = "".join(str.split())
			return Decimal(str)
		except AttributeError:
			return 0

	def save_to_product(self, defaults, category):
		product, create = Product.objects.update_or_create(name=defaults['name'], 
											shop=self.shop, city=self.city, defaults=defaults)

		for cat in category:
			category, create = Category.objects.get_or_create(name=cat)
			product.categories.add(category)

		price = Price(price = defaults['current_price'], product = product) 
		price.save()

