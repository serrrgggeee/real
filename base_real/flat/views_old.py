#  data = {'not_first_floor':False, 'houseroom':[{'lower': 1, 'upper':2}]}
# serializer = FlatSerializer(data = data)
# serializer.initial_data
# {'not_first_floor': False, 'houseroom': [{'lower': 1, 'upper': 2}]}
# serializer.is_valid()
# True
# serializer.save()
# {'not_first_floor': False}
# <Flat: Flat object (33)>


from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from psycopg2.extras import NumericRange

from base_real.serializers import FlatSerializer
from base_real.models import Flat

class FlatView(APIView):
	def get(self, request, flat_id=None, format=None):
		if flat_id:
			flat = get_object_or_404(Flat, pk=flat_id)
		else:
			flat = Flat.objects.all()
		serialized_Flat = FlatSerializer(flat, many=True)
		return Response(serialized_Flat.data)

	def update(self, request, *args, **kwargs):
		data = request.DATA
		qs = Flat.objects.filter(student=1)
		serializer = FlatSerializer(qs, data=data, many=True)

		if serializer.is_valid():
			serializer.save()

		return Response(serializer.data)

	def post(self, request, format=None):
		lower = request.data['houseroom']['lower'] 
		upper = request.data['houseroom']['upper']
		
		request.data['houseroom'] = [{'lower':lower, 'upper':upper}]
		print(request.data)
		serializer = FlatSerializer(data = request.data)
		print(serializer.initial_data)
		if serializer.is_valid():
			print(serializer.is_valid())
			serializer.save()
			return Response(serializer.data, status= status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		flat = Flat.objects.filter(student=2773951)
		flat.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)



