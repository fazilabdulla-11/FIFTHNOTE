from django.contrib import admin
from .models import Perfume, PerfumeImage, Order, OrderItem


class PerfumeImageInline(admin.TabularInline):
    model = PerfumeImage
    extra = 7
    max_num = 7


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'price_20ml',
        'price_50ml',
        'created_at',
    )

    search_fields = ('name', 'brand')

    fields = (
        'name',
        'brand',
        'description',
        'price_20ml',
        'price_50ml',
        'image_url',
        'image_20ml',
    )

    inlines = [PerfumeImageInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'pincode',
        'total',
        'created_at',
    )

    search_fields = ('name', 'phone', 'pincode')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'perfume',
        'size',
        'quantity',
        'price',
    )

    search_fields = ('perfume__name',)