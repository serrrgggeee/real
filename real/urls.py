"""Main url."""
import debug_toolbar
from django.contrib import admin
from django.conf.urls import url
from rest_framework import routers
from django.urls import include, path

from rest_framework.authtoken import views as auth_views


from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api/', include("base_real.flat.urls")),
    url(r'^account/', include("accounts.urls")),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-token-auth/', auth_views.obtain_auth_token, name='api-token-auth'),
    path('__debug__/', include(debug_toolbar.urls))
]
