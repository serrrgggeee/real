"""base url."""
from django.urls import path
from .views import (
    ListAPIView,
    DetailAPIView,
    UpdateAPIView,
    DeleteAPIView,
    CreateAPIView
)

app_name = (__package__) + "-api"
urlpatterns = [
    path(r'', ListAPIView.as_view(), name='list'),
    path(r'(?P<pk>\d+)/', DetailAPIView.as_view(), name='detail'),
    path('create/', CreateAPIView.as_view({'post': 'create'}), name='create'),
    # path(r(?P<slug>[\w-]+)/', DetailAPIView.as_view(), name='detail'),
    path(r'(?P<pk>\d+)/edit/', UpdateAPIView.as_view(), name='edit'),
    path(r'(?P<pk>\d+)/delete/', DeleteAPIView.as_view(), name='delete')
]
