from core.models import Product , Category , Vendor , CartOrder , CartOrderItem, ProductImages , ProductReview , Wishlist , Address
from django.db.models import Min, Max 
from django.contrib import messages

# def default(request):
#     categories = Category.objects.all()
#     address = Address.objects.get(user=request.user)
#     return {
#         'categories': categories,
#         'address': address,
#     }



def default(request):
    categories = Category.objects.all()
    address = None  # Default to None if user is anonymous or has no address

    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))


    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to login before accessing your wishlist.")
        wishlist = 0



    if request.user.is_authenticated:  # Ensure user is logged in
        try:
            address = Address.objects.filter(user=request.user)
        except Address.DoesNotExist:
            address = None  # Handle case where no address is found

    return {
        'categories': categories,
        'wishlist': wishlist,
        'address': address,
        'vendors': vendors,
        'min_max_price': min_max_price,
    }
