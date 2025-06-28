from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404 , redirect
from taggit.models import Tag
from core.models import Product , Category , Vendor , CartOrder , CartOrderItem, ProductImages , ProductReview , Wishlist , Address
from userauths.models import ContactUs, Profile
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.core import serializers
from django.utils import timezone
from datetime import timedelta         # ← أضف هذا السطر
from django.db.models.functions import TruncMonth   # ← هذا السطر يعرّف TruncMonth
import re
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm                                                                                                                           
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count
import calendar
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth
from django.db.models import Sum ,F
from .utils import get_recommended_products_for_user
import sys
sys.path.append(r'D:\New folder (42)\graduation-project-main\venv2\Lib\site-packages')
from textblob import TextBlob



def dashboard_view(request):
    paid_orders = CartOrder.objects.filter(paid_status=True)

    total_revenue    = paid_orders.aggregate(total=Sum('price'))['total'] or 0
    total_orders     = paid_orders.count()
    total_products   = Product.objects.count()
    total_categories = Category.objects.count()

    now = timezone.now()
    monthly_earning = paid_orders.filter(
        order_date__year=now.year,
        order_date__month=now.month
    ).aggregate(total=Sum('price'))['total'] or 0

    # بيانات الشارت 1 — Revenue شهريًا لآخر 6 أشهر
    six_months_ago = now - timedelta(days=30*5)
    monthly_qs = (
        paid_orders
        .filter(order_date__gte=six_months_ago)
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total=Sum('price'))
        .order_by('month')
    )
    chart_labels = [m['month'].strftime('%b') for m in monthly_qs]
    chart_data   = [float(m['total'] or 0) for m in monthly_qs]

    # بيانات الشارت 2 — Revenue حسب vendor.address
    area_qs = (
        Product.objects
        .values(address=F('vendor__address'))
        .annotate(revenue=Sum('price'))
        .order_by('-revenue')
    )
    area_labels = [item['address'] for item in area_qs]
    area_data   = [float(item['revenue'] or 0) for item in area_qs]

    context = {
        'total_price':      total_revenue,
        'total_orders':     total_orders,
        'total_products':   total_products,
        'total_categories': total_categories,
        'monthly_earning':  monthly_earning,
        'chart_labels':     chart_labels,
        'chart_data':       chart_data,
        'area_labels':      area_labels,
        'area_data':        area_data,
    }
    return render(request, 'core/dashboard-back.html', context)

# Create your views here.
def index(request):
    # products = product.objects.all().order_by('-id')
    recommended = get_recommended_products_for_user(request.user)
    products = Product.objects.filter( product_status='published',featured=True)
    top_selling = Product.objects.filter(product_type='top_selling', available=True)[:4]
    trending = Product.objects.filter(product_type='trending', available=True)[:4]
    recently_added = Product.objects.filter(product_type='recent', available=True).order_by('-date')[:4]
    top_rated = Product.objects.filter(product_type='top_rated', available=True)[:4]
    context = {
        'recommended': recommended,
        'products' : products,
        'top_selling': top_selling,
        'trending': trending,
        'recently_added': recently_added,
        'top_rated': top_rated,
    }
    return render(request, 'core/index.html', context) 
def vendor_guide(request):


    return render(request, 'core/vendor-guide.html')
def blog_category(request):


    return render(request, 'core/blog-category-big.html')
def product_list_view(request):
    products = Product.objects.filter( product_status='published')
    tags = Tag.objects.all()
    
    context = {
        'products' : products,
        'tags' : tags,
    }
    return render(request, 'core/product-list.html', context)


def tag_list(request, tag_slug=None):
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = Product.objects.filter(tags__in=[tag])

    return render(request, "core/tag.html", {
        "products": products,
        "tag": tag
    })


def category_list_view(request):
    categories = Category.objects.all()
    # categories = category.objects.all().annotate(product_count=Count('product'))

    context = {
        'categories' : categories,
    }
    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)

    context = {
        'category' :category,
        'products' :products,
    }
    return render(request, 'core/category-product-list.html', context)






def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors' : vendors,
    }
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published')
    context = {
        'vendor' : vendor,
        'products' : products
    }
    return render(request, 'core/vendor-detail.html', context)



def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews related to a product 
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product Review form
    review_form = ProductReviewForm()

    make_review = True

    total_reviews = ProductReview.objects.filter(product=product).count()
    positive_reviews = ProductReview.objects.filter(product=product, polarity__gt=0.1).count()

    if total_reviews > 0:
        positive_percentage = (positive_reviews / total_reviews) * 100
    else:
        positive_percentage = 0

    # if request.user.is_authenticated:
    #     user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

    #     if user_review_count > 0:
    #         make_review = False

    # Count each rating for the product
    rating_counts = ProductReview.objects.filter(product=product).values('rating').annotate(count=Count('rating'))

    # Build a dictionary for easier access
    rating_distribution = {star: 0 for star in range(1, 6)}  # 1 to 5
    total_reviews = ProductReview.objects.filter(product=product).count()

    for entry in rating_counts:
        rating_distribution[entry['rating']] = entry['count']

    # Convert to percentage
    rating_percentages = {}
    for star, count in rating_distribution.items():
        if total_reviews > 0:
            rating_percentages[str(star)] = round((count / total_reviews) * 100, 1)
        else:
            rating_percentages[str(star)] = 0
    
    star_percent = 0

    if average_rating["rating"]:
        star_percent = round((average_rating["rating"] / 5) * 100, 1)


    p_image = product.p_images.all()
    
    context = {
        "p":product,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
        "positive_percentage": round(positive_percentage, 2),
        "rating_percentages": rating_percentages,
        "star_percent": star_percent,
    }
    return render(request, "core/product-detail.html", context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag,
    }

    return render(request, "core/tag.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review_text = request.POST['review']
    rating = request.POST['rating']

    # Sentiment analysis
    sentiment = TextBlob(review_text).sentiment.polarity
    if sentiment > 0.1:
        sentiment_label = "Positive"
    elif sentiment < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    # Save the review
    review = ProductReview.objects.create(
    user=user,
    product=product,
    review=review_text,
    rating=rating,
    sentiment=sentiment_label,
    polarity=sentiment,
)

    # Attach sentiment to the review (optional: save in DB if you add a field)
    context = {
        'user': user.username,
        'review': review_text,
        'rating': rating,
        'sentiment': sentiment_label,
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    
    positive_reviews = ProductReview.objects.filter(product=product, sentiment='Positive').count()
    total_reviews = ProductReview.objects.filter(product=product).count()
    like_percentage = round((positive_reviews / total_reviews) * 100, 2) if total_reviews else 0

    return JsonResponse({
        'bool': True,
        'context': context,
        'average_reviews': average_reviews,
        'like_percentage': like_percentage
    })



def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context = {
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)



def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

     
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)


    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])]  = {
        'title': request.GET['title'],
        'qty':  request.GET['qty'],
        'price': float(request.GET['price']),
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }  
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})



def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html" , {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount } )
    else:
        messages.warning(request,"Your cart is empty")
        return redirect("core:index")



def delete_item_from_cart(request):  
    product_id = str(request.GET['id'])  
    if 'cart_data_obj' in request.session:  
        if product_id in request.session['cart_data_obj']:  
            cart_data = request.session['cart_data_obj']  
            del request.session['cart_data_obj'][product_id]  
            request.session['cart_data_obj'] = cart_data  
    
    cart_total_amount = 0  
    if 'cart_data_obj' in request.session:  
        for pid, item in request.session['cart_data_obj'].items():  
            cart_total_amount += int(item['qty']) * float(item['price'])  
    
    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount } )  
    return JsonResponse({ "data":context , 'totalcartitems':len(request.session['cart_data_obj']) })



def update_cart(request):  
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty'] 
    #product_qty = request.GET.get('qty') 

    if 'cart_data_obj' in request.session:  
        if product_id in request.session['cart_data_obj']:  
            cart_data = request.session['cart_data_obj']  
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data  
            

    cart_total_amount = 0  
    if 'cart_data_obj' in request.session:  
        for pid, item in request.session['cart_data_obj'].items():  
            cart_total_amount += int(item['qty']) * float(item['price'])  
    
    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount } )  
    return JsonResponse({ "data":context , 'totalcartitems':len(request.session['cart_data_obj']) })

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0

    # Checking if cart_data_obj in session
    if 'cart_data_obj' in request.session:

        # Getting total amount for Paypal Amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        # Create Order Object
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount
        )

        # Getting total amount for The Cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderItem.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),  # INVOICE_NO-5
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )




    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": cart_total_amount,
        "item_name": "Order-Item-No-" + str(order.id),
        "invoice": "INV_NO-" + str(order.id),
        "currency_code": "USD",
        "notify_url":  "https://{}/{}".format(host, reverse("core:paypal-ipn")),
        "return_url":  "http://{}/{}".format(host, reverse("core:payment-completed")),
        "cancel_return": "http://{}/{}".format(host, reverse("core:payment-failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)


    # cart_total_amount = 0  
    # if 'cart_data_obj' in request.session:  
    #     for pid, item in request.session['cart_data_obj'].items():  
    #         cart_total_amount += int(item['qty']) * float(item['price'])  

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "There are multiple address, only one should be Activated")
        active_address = None
    
    return render(request, "core/checkout.html" , {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount , 'paypal_payment_button':paypal_payment_button, "active_address":active_address } )

@login_required
def payment_completed_view(request):
    cart_total_amount = 0  
    if 'cart_data_obj' in request.session:  
        for pid, item in request.session['cart_data_obj'].items():  
            cart_total_amount += int(item['qty']) * float(item['price'])  
    return render(request, "core/payment-completed.html" , {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']) , 'cart_total_amount':cart_total_amount })
    


 
@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')





@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    addresses = Address.objects.filter(user=request.user)  # Keep it as a queryset


    orders = (
    CartOrder.objects.filter(user=request.user)  # Filter orders for the logged-in user
    .annotate(month=ExtractMonth("order_date"))
    .values("month")
    .annotate(count=Count("id"))
    .values("month", "count")
    )
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i["count"])


    if request.method == "POST":
        address_text = request.POST.get("address")  
        mobile = request.POST.get("mobile")

        # Check if the exact same address already exists
        if not Address.objects.filter(user=request.user, address=address_text, mobile=mobile).exists():
            Address.objects.create(
                user=request.user,
                address=address_text,
                mobile=mobile,
            )
            messages.success(request, "Address Added Successfully.")
        else:
            messages.warning(request, "This address already exists.")

        return redirect("core:dashboard") 
    else:
        print("Error")

    user_profile = Profile.objects.get(user=request.user)


    context = {
        "user_profile": user_profile,
        "orders_list": orders_list,
        "addresses": addresses,  # Keep multiple addresses
        "orders":orders,
        "month":month,
        "total_orders":total_orders,
    }
    return render(request, 'core/dashboard.html', context)



def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItem.objects.filter(order=order)
    context = {
        "order_items": order_items
    }
    return render(request, 'core/order-detail.html', context)


def make_address_default(request):
    id = request.GET["id"]
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})




@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.all()
    context = {
        "w":wishlist
    }
    return render(request, "core/wishlist.html", context)


def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)



def remove_wishlist(request):
        pid = request.GET['id']
        wishlist = Wishlist.objects.filter(user=request.user)

        product = Wishlist.objects.get(id=pid)
        product.delete()

        context = {
            "bool": True,
            "w":wishlist
        }
        wishlist_json = serializers.serialize('json', wishlist)

        data = render_to_string("core/async/wishlist-list.html", context)
        return JsonResponse({"data": data, "w":wishlist_json})    



# Other pages
def contact(request):
    return render(request, "core/contact.html")


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email'] 
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name = full_name,
        email = email,
        phone = phone,
        subject = subject,
        message = message,
    )

    data = {
        "bool": True,
        "message": "Message sent successfully"
    }
    return JsonResponse({"data":data})



def about_us(request):
    return render(request, "core/about_us.html")


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_of_service(request):
    return render(request, "core/terms_of_service.html")

def vendor_guide(request):
    return render(request, "core/vendor_guide.html")


def blog_full(request):
    return render(request, "core/blog_full.html")


def chatbot_view(request):
    user_message = request.GET.get("message", "").strip().lower()
    response = handle_user_message(user_message)
    return JsonResponse({"reply": response})


def handle_user_message(message):
    # Clean message (no punctuation)
    cleaned_msg = re.sub(r'[^\w\s]', '', message)

    # Define intents and their keywords
    intents = {
        "price": ["price", "cost", "how much", "worth"],
        "products": ["products", "show", "list", "available", "have"],
        "categories": ["categories", "types", "sections", "kinds", "category"]
    }

    # Determine intent
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in cleaned_msg:
                return intent_handler(intent, cleaned_msg)

    # Default fallback
    return (
        "Sorry, I didn't understand your question. You can ask:<br>"
        "- What is the price of product X?<br>"
        "- What products are available?<br>"
        "- What categories do you have?"
    )


def intent_handler(intent, message):
    if intent == "price":
        return get_product_price(message)
    elif intent == "products":
        return list_products()
    elif intent == "categories":
        return list_categories()
    return "Intent not recognized."


def get_product_price(message):
    # Try extracting the product name more reliably
    # Look for common phrases and split after them
    patterns = [
        r"(?:how much (?:is|are) )(?P<product>.+)",
        r"(?:what(?:'s| is) the price of )(?P<product>.+)",
        r"(?:price of )(?P<product>.+)",
        r"(?:price )(?P<product>.+)",
        r"(?:cost of )(?P<product>.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            query = match.group("product").strip()
            break
    else:
        # Fallback to entire message
        query = message.strip()

    if not query:
        return "Please specify the product name."

    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        available=True
    )[:3]

    if not products:
        return f"No products found matching '{query}'."

    if len(products) > 1:
        listing = "<br>".join([f"{p.title} - {p.price} EGP" for p in products])
        return f"Found multiple results:<br>{listing}<br>Please be more specific."

    return f"The price of <b>{products[0].title}</b> is <b>{products[0].price} EGP</b> 💵."

def list_products():
    products = Product.objects.filter(available=True).order_by('-date')[:5]
    if not products:
        return "No available products found."
    listing = "<br>- " + "<br>- ".join([p.title for p in products])
    return f"Here are the latest products:{listing}"


def list_categories():
    categories = Category.objects.all()[:5]
    if not categories:
        return "No categories found."
    listing = "<br>- " + "<br>- ".join([c.title for c in categories])
    return f"Here are some main categories:{listing}"

@login_required
def clean_cart_view(request):
    if 'cart_data_obj' in request.session:
        cleaned_cart = {}
        for pid, item in request.session['cart_data_obj'].items():
            try:
                float(item['price'])  # This will throw ValueError if invalid
                cleaned_cart[pid] = item
            except ValueError:
                print(f"Removed invalid item: {item}")
        
        request.session['cart_data_obj'] = cleaned_cart
        request.session.modified = True
        return redirect('core:cart')  # or wherever your cart is shown

    return redirect('core:index')  # fallback





