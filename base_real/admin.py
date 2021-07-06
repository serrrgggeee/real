from django.contrib import admin
from .models import Flat, Underground, TypeObject, Closet

admin.site.register(Underground)
admin.site.register(TypeObject)
admin.site.register(Closet)
admin.site.register(Flat)
