from django.db.models import Count, Q
from .models import Product, Wishlist

def get_recommended_products_for_user(user, top_n=6):
    if not user.is_authenticated:
        return Product.objects.filter(status=True, available=True).order_by('-price')[:top_n]

    liked_products = Wishlist.objects.filter(user=user).values_list('product_id', flat=True)

    if liked_products:
        # Step 1: Based on other users' wishlists
        collaborative = Product.objects.filter(
            wishlist__product__in=liked_products
        ).exclude(
            id__in=liked_products
        ).annotate(
            common_likes=Count('wishlist')
        ).order_by('-common_likes')[:top_n]

        if collaborative.exists():
            return collaborative

        # Step 2: Based on categories of liked products
        liked_categories = Product.objects.filter(id__in=liked_products).values_list('category', flat=True)
        category_based = Product.objects.filter(
            category__in=liked_categories,
            available=True
        ).exclude(
            id__in=liked_products
        ).order_by('-date')[:top_n]

        if category_based.exists():
            return category_based

    # Step 3: Default fallback - top-rated or recent
    return Product.objects.filter(available=True).order_by('-date')[:top_n]
