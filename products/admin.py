from django.contrib import admin
from .models import Category, Product, Tags, Type


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'edition',
        'category',
        'price',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
    )


class TypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'image',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Type, TypeAdmin)