# -*- coding: utf-8 -*-

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from my_magazine.models import Product, Comments, Category, Brands, Author, Home, Keywords



# Register your models here.
class ProductInline(admin.StackedInline):
    model = Comments
    extra = 1

class HomeAdmin(admin.ModelAdmin):
    fields = ['home_title', 'home_text', 'home_date', 'home_image', 'video']
    list_display = ('home_title', 'home_date', 'home_image', 'bit_home')


class ProductAdmin(admin.ModelAdmin):
    fields = ['product_title', 'product_price', 'product_img', 'product_text', 'product_stock', 'product_video', 'category', 'keywords', 'brands', 'author']
    list_display = ('product_title', 'product_img', 'bit', 'category', 'brands', 'author', 'product_price', 'product_stock', 'product_created', 'product_updated', 'product_available')
    inlines = [ProductInline]
    list_filter = ['category']
    search_fields = ['product_title']
    list_editable = ['product_price', 'product_stock', 'product_available']

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'parent']

class KeywordsAdmin(admin.ModelAdmin):
    fields = ['name']

class BrandsAdmin(admin.ModelAdmin):
    fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
    fields = ['name', 'author_image']
    list_display = ['name', 'author_image']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Home, HomeAdmin)