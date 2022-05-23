from django.contrib import admin

from apps.models import Category, Product, Profile

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)