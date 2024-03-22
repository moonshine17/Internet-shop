from django.contrib import admin

from goods.models import Categories, Products

# Register your models here.
admin.site.register(Categories)
admin.site.register(Products)