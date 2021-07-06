import json

from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,

)
from rest_framework import viewsets

from rest_framework.response import Response

from psycopg2.extras import NumericRange

from .serializers import (
    ListSerializer,
    DetailSerializer,
    CreateUpdateSerializer
)

from .pagination import LimitOffsetPagination, PageNumberPagination

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .permissions import IsOwnerOrReadOnly

from base_real.models import Flat, Underground

from rest_framework.authentication import TokenAuthentication


class CreateAPIView(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = CreateUpdateSerializer
    permission_classes = [IsAuthenticated]


class DetailAPIView(RetrieveAPIView):
    queryset = Flat.objects.all()
    serializer_class = DetailSerializer
    # lookup_field = 'slug'
    # lookup_url_kwarg = "abc"


class UpdateAPIView(RetrieveUpdateAPIView):
    queryset = Flat.objects.all()
    serializer_class = CreateUpdateSerializer
    # lookup_field = 'slug'
    # lookup_url_kwarg = "abc"
    # def perform_update(self, serializer):
    #   serializer.save(user=self.request.user, title="my title")


class DeleteAPIView(DestroyAPIView):
    queryset = Flat.objects.all()
    serializer_class = DetailSerializer
    # lookup_field = 'slug'
    # lookup_url_kwarg = "abc"


class ListAPIView(ListAPIView):
    # queryset = Flat.objects.all()
    authentication_classes = (TokenAuthentication,)
    # curl -H "Accept: application/json" -H "AUTHORIZATION: Token 16cb7f9fe1f3abdd962dc670bf3076b8e1649319"    http://127.0.0.1:8000/api

    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['not_first_floor']
    # LimitOffsetPagination #PageNumberPagination
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Flat.objects.all()
        # query = self.request.Get.get("q")
        # if query:
        #   queryset_list = queryset_list.filter(
        #       Q(title__icontains=query)|
        #       Q(content__icontains=query)|
        #       Q(user__first_name__icontains=query)|
        #       Q(title__last_name__icontains=query)
        #       ).ditinct()
        return queryset_list

        # 127.0.0.1/api/?limit=2&offset=1&search=new%20flat&q=here&ordering=title
        # 127.0.0.1/api/?search=new%20flat&q=here&ordering=-title
        # curl -X DELETE -H 'Accept: application/json; indent=4' -u real:real http://127.0.0.1:8000/api/44/delete/
        # curl -H 'Accept: application/json; indent=4' -u real:real http://127.0.0.1:8000/api/
        #curl - X POST - H 'Accept: application/json; indent=4' - u real: real http: // 127.0.0.1: 8000/api/create / \
        #--data 'underground={"name": "new_name"}&type_object=1&total_area={"lower": "1", "upper": "15"}&houseroom={"lower": "1", "upper": "13"}&area_kitchen={"lower": "1", "upper": "15"}&material_building=кирпич&floor={"lower": "1", "upper": "15"}&not_first_floor=true&not_last_floor=true&count_floor={"lower": "1", "upper": "15"}&count_room=1&planing=1&closet=1&balcony=true&loggia=true&with_photo=true&hypothec=true&bargain=true&exchange=true&net_sale=true' \
