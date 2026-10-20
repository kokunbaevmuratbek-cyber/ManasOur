from django.contrib import admin
from .models import Place, PlaceImage, Category

# Register your models here.
admin.site.register(Place)
admin.site.register(PlaceImage)
admin.site.register(Category)
