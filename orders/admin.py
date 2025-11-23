from django.contrib import admin
from .models import Payment, Order, OrderProduct
from django.utils.html import format_html

class OrderProdcutInline(admin.TabularInline):
    def thumbnail(self, object):
        return format_html('<img style="border-radius:10px; width:80px; height:80px; object-fit: cover;" src="{}">'.format(object.product.image.url))
    thumbnail.short_description = 'Product'
    model = OrderProduct
    readonly_fields = ['thumbnail','product','variations','product_price', 'quantity','user','payment', 'ordered']
    extra = 0

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status_badge', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['payment_id', 'user__email']
    readonly_fields = ['payment_id', 'created_at']
    
    def status_badge(self, obj):
        if obj.status == 'Completed':
            return format_html('<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">COMPLETED</span>')
        elif obj.status == 'Pending':
            return format_html('<span style="background: #ffc107; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">PENDING</span>')
        return format_html('<span style="background: #dc3545; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">FAILED</span>')
    status_badge.short_description = 'Status'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'formatted_total', 'status_badge', 'order_date']
    list_filter = ['is_ordered', 'status', 'created_at']
    list_per_page = 20
    inlines = [OrderProdcutInline]
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'payment')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'phone', 'email')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'order_note'),
            'classes': ('collapse',)
        }),
        ('Order Summary', {
            'fields': ('order_total', 'tax', 'status', 'ip', 'is_ordered')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def formatted_total(self, obj):
        return format_html('<span style="color: #28a745; font-weight: bold; font-size: 14px;">${}</span>', obj.order_total)
    formatted_total.short_description = 'Total'
    
    def status_badge(self, obj):
        status_colors = {
            'New': '#007bff',
            'Accepted': '#28a745', 
            'Completed': '#28a745',
            'Cancelled': '#dc3545'
        }
        color = status_colors.get(obj.status, '#6c757d')
        return format_html('<span style="background: {}; color: white; padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: bold;">{}</span>', color, obj.status.upper())
    status_badge.short_description = 'Status'
    
    def order_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    order_date.short_description = 'Order Date'

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product_image', 'product', 'user', 'quantity', 'product_price', 'ordered_status']
    list_filter = ['ordered', 'created_at']
    search_fields = ['product__name', 'user__email']
    
    def product_image(self, obj):
        if obj.product.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 8px; object-fit: cover;" />', obj.product.image.url)
        return "No Image"
    product_image.short_description = 'Image'
    
    def ordered_status(self, obj):
        if obj.ordered:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">ORDERED</span>')
        return format_html('<span style="background: #ffc107; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">PENDING</span>')
    ordered_status.short_description = 'Status'