# admin.py
from django.contrib import admin
from .models import Tovar


class TovarAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_sng','price_EUROPE_AMERICA','price_Africa_Australia', 'category', 'created_at', 'updated_at')

    # Возможность фильтровать товары по категории
    list_filter = ('category',)

    # Поиск по имени товара
    search_fields = ('name',)

    fields = ('name',  'price_sng','price_EUROPE_AMERICA','price_Africa_Australia',  'description', 'category', 'image')

    # Добавляем возможность сортировки по цене
    ordering = ( 'price_sng','price_EUROPE_AMERICA','price_Africa_Australia',)


# Регистрируем модель Tovar в админке
admin.site.register(Tovar, TovarAdmin)
