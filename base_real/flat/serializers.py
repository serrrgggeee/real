from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    HyperlinkedIdentityField,
    SlugRelatedField
)

from base_real.models import (
    Flat,
    Underground,
    TypeObject,
    Closet
)

fields = [
    'pk',
    'underground',
    'type_object',
    'total_area',
    'houseroom',
    'area_kitchen',
    'material_building',
    'floor',
    'not_first_floor',
    'not_last_floor',
    'count_floor',
    'count_room',
    'planing',
    'closet',
    'balcony',
    'loggia',
    'with_photo',
    'hypothec',
    'bargain',
    'exchange',
    'net_sale'
]


class UndergroundSerializer(ModelSerializer):
    class Meta:
        model = Underground
        fields = ('pk', 'name',)


class ClosetSerializer(ModelSerializer):
    class Meta:
        model = Closet
        fields = ('pk', 'name',)


class TypeObjectSerializer(ModelSerializer):
    class Meta:
        model = TypeObject
        fields = ('pk', 'name')


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


class ListSerializer(ModelSerializer, MixinSerializer):
    fields.extend(['url', 'pk', 'delete_url'])

    class Meta:
        model = Flat
        fields = fields


class DetailSerializer(ModelSerializer, MixinSerializer):
    underground = SerializerMethodField()
    closet = SerializerMethodField()
    fields.extend(['url', 'pk'])

    class Meta:
        model = Flat
        fields = fields

    def get_underground(self, obj):
        underground = obj.underground.all()
        return [{u.name, u.pk} for u in underground]

    def get_closet(self, obj):
        closet = obj.closet.all()
        return [{c.name, c.pk} for c in closet]


class CreatableSlugRelatedField(SlugRelatedField):

    def to_internal_value(self, data):
        try:
            value = self.get_queryset().get_or_create(**{self.slug_field: data})[0]
            return value
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field,
                      value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class CreateUpdateSerializer(ModelSerializer, MixinSerializer):
    # underground = UndergroundSerializer()
    underground = CreatableSlugRelatedField(
        slug_field='name', many=True, queryset=Underground.objects.all(),)

    class Meta:
        model = Flat
        fields = fields

    def create(self, validated_data):
        underground = validated_data.pop('underground')
        closet = validated_data.pop('closet')
        flat_instance = Flat.objects.create(**validated_data)

        for u in underground:
            underground_instance, created = Underground.objects.get_or_create(name=u)
            flat_instance.underground.add(underground_instance)

        for c in closet:
            flat_instance.closet.add(c)
        return flat_instance
