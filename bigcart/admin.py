from django.contrib import admin
from .models import Order, OrderItem, Customer, Product, Cart, OrderItem, Coupon

admin.site.register(Product)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created_date', 'updated']
    list_filter = ['paid', 'created_date', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(OrderItem)

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
admin.site.register(Coupon, CouponAdmin)
