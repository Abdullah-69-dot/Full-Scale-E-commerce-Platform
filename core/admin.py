from django.contrib import admin
from core.models import Product , Category , Vendor , CartOrder , CartOrderItem, ProductImages , ProductReview , Wishlist , Address
from django.contrib.sessions.models import Session
from django.utils.timezone import now

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
class productAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','title','product_image', 'price','category','vendor', 'featured', 'product_status', 'pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ["paid_status" , "product_status"]
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemAdmin(admin.ModelAdmin):    
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'review']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address','status']
    list_display = ['user', 'address','status']

@admin.action(description="Clear cart_data_obj from selected sessions")
def clear_cart_data(modeladmin, request, queryset):
    for session in queryset:
        data = session.get_decoded()
        if 'cart_data_obj' in data:
            data['cart_data_obj'] = {}
            session.session_data = Session.objects.encode(data)
            session.save()
    modeladmin.message_user(request, "Selected session carts cleared.")

@admin.action(description="Clean malformed prices from selected sessions")
def clean_malformed_prices(modeladmin, request, queryset):
    cleaned_sessions = 0
    cleaned_items = 0
    for session in queryset:
        data = session.get_decoded()
        if 'cart_data_obj' in data:
            cleaned_cart = {}
            for p_id, item in data['cart_data_obj'].items():
                try:
                    # Validate and clean price string
                    price = item['price'].strip()
                    if '.' in price:
                        price = price.split('.')[0] + '.' + price.split('.')[1][:2]
                    price_float = float(price)
                    if price_float > 0:
                        cleaned_cart[p_id] = item
                except (ValueError, TypeError):
                    cleaned_items += 1
                    continue
            
            if cleaned_cart != data['cart_data_obj']:
                data['cart_data_obj'] = cleaned_cart
                session.session_data = Session.objects.encode(data)
                session.save()
                cleaned_sessions += 1
    
    message = f"Cleaned {cleaned_items} malformed items from {cleaned_sessions} sessions."
    modeladmin.message_user(request, message)

class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date']
    actions = [clear_cart_data, clean_malformed_prices]

admin.site.register(Session, SessionAdmin)



admin.site.register(Product, productAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
