from django.shortcuts import render

from django.http import Http404

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login as django_login, logout as django_logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

from .serializers import UserSerializer, LoginSerializer

class LoginAPIView(APIView):
	#authentication_classes = (TokenAuthentication,)
	serializer_class = UserSerializer
	#permission_classes = [IsAuthenticated]

	#def get_serializer_context(self):
	#	username = self.request.POST.get('username')
	#	print(username)
	#	return {'request': self.request}

	def post(self, request):
		#curl -X POST -H "Accept: application/json; indent=4" -H "AUTHORIZATION: Token 16cb7f9fe1f3abdd962dc670bf3076b8e1649319"  http://127.0.0.1:8000/account/login/
		#try:
		#	queryset = User.objects.get(username=self.request.data['username'])
		#except User.DoesNotExist:
		#queryset = AnonymousUser()
		#data = {
		#	'username': queryset.username
		#}
		#print(data)
		#serializer = UserSerializer(data=data)
		#print(dir(serializer))
		#if serializer.is_valid():
		#	print(serializer)
		#return Response(status=status.HTTP_201_CREATED)
		#print(serializer.errors)
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		django_login(request, user)
		token, created = Token.objects.get_or_create(user=user)
		return Response({'token': token.key}, status=200)
		#curl -X POST -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/account/login/ --data 'username=serrrgggeee&password=Tktyf,firjdf1'
		#{
		#    "username":"serrrgggeee",
		#    "email":"serrrgggeee@mail.ru",
		#    "password":"Tktyf,firjdf1"
		#}


class LogoutAPIView(APIView):
	#authentication_classes = (TokenAuthentication,)

	def post(self, request):
		django_logout(request)
		return Response(status=204)