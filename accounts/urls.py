from django.conf.urls import url
from .views import (
	LoginAPIView,
	LogoutAPIView
	)

app_name="accounts"
urlpatterns = [
    url(r'^login/$', LoginAPIView.as_view(), name='login'),
    url(r'^logout/$', LogoutAPIView.as_view(), name='logout')
]

