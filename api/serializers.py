from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
	HyperlinkedIdentityField,
	HyperlinkedModelSerializer
	)


class UserSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

# class CreateUpdateSerializer(ModelSerializer):
# 	class Meta:
# 		model = Flat
# 		fields = [
# 			'houseroom',
# 			'not_first_floor'
# 		]
