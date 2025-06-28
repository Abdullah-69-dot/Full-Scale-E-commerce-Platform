from django.urls import path ,include
from core.views import chatbot_view, dashboard_view , blog_category,vendor_guide,category_list_view, category_product_list_view, index,product_detail_view , product_list_view, vendor_list_view, vendor_detail_view, tag_list, ajax_add_review, search_view, filter_product , add_to_cart , cart_view ,delete_item_from_cart , update_cart , checkout_view , payment_completed_view ,payment_failed_view, customer_dashboard, order_detail, make_address_default, wishlist_view, add_to_wishlist, remove_wishlist, contact, about_us, purchase_guide, privacy_policy, terms_of_service, ajax_contact_form, blog_full, clean_cart_view
app_name = "core"
urlpatterns = [

    #Homepage
    path('chatbot/',chatbot_view, name='chatbot'),
    path("",index, name='index'),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    path('dash/', dashboard_view, name='dashboard-vendor'),
    #Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),
    path("blog/category", blog_category, name="blog-category"),
    
    #Vendor
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),
    path("vendors/guide", vendor_guide, name="vendor-guide"),
    #Tags 
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    # Add Review
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review" ),

    # Search 
    path("search/", search_view, name="search"),
    # Filter product URL
    path("filter-products/", filter_product, name="filter-product"),
    # add to cart URL
    path("add-to-cart/", add_to_cart , name="add-to-cart" ),
    # cart page URL
    path("cart/",cart_view,name="cart"),
    # Delete Item from cart
    path("delete-from-cart/",delete_item_from_cart,name="delete-from-cart"),
    # update cart
    path("update-cart/",update_cart,name="update-cart"),
    # checkout URL
    path("checkout/",checkout_view,name="checkout"), 
    # paypal URL 
    path("paypal/",include('paypal.standard.ipn.urls')),
    # payment successful 
    path("payment-completed/",payment_completed_view,name="payment-completed"),
    # payment failed 
    path("payment-failed/",payment_failed_view,name="payment-failed"),
    # dashboard Url
    path("dashboard/", customer_dashboard, name="dashboard"),
    # Order Detail Url
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),
    # make_address_default
    path("make-default-address", make_address_default, name="make-default-address"),
    # wishlist page
    path("wishlist/", wishlist_view, name="wishlist"),
    #adding to wishlist
    path("add-to-wishlist", add_to_wishlist, name="add-to-wishlist"),
    #removing from wishlist
    path("wishlist/remove-from-wishlist", remove_wishlist, name="remove-from-wishlist"),
    #contact page
    path("contact/", contact, name="contact"),
    #ajax contact page
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),
    #about_us page
    path("about_us/", about_us, name="about_us"),
    #purchase_guide page
    path("purchase_guide/", purchase_guide, name="purchase_guide"),
    #privacy_policy page
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    #contact page
    path("terms_of_service/", terms_of_service, name="terms_of_service"),
    #vendor guide page
    path("vendor_guide/", vendor_guide, name="vendor_guide"),
    #blog_full page
    path("blog_full/", blog_full, name="blog_full"),
    #clean cart
    path("clean-cart/", clean_cart_view, name="clean-cart"),
    #tags
    path("tag/<slug:tag_slug>/", tag_list, name="tag"),
    

]
