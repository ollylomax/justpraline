from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'cart_instance',
                       'payment_id')

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'address_line1',
              'address_line2', 'county', 'postcode', 'country',
              'delivery_cost', 'order_total', 'grand_total',
              'cart_instance', 'payment_id', 'user_profile',
              'has_artwork')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total', 'has_artwork')

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
