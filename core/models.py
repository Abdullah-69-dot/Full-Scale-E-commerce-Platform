from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager 
from ckeditor_uploader.fields import RichTextUploadingField



STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)
STATUS= (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)
RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
    
)
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefgh12345')
    title = models.CharField(max_length=100, default='Food')
    image = models.ImageField(upload_to='category', default='category.jpg')

    class Meta:
        verbose_name_plural = 'categories'
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'%(self.image.url))
    def __str__(self):
        return self.title    
class Tags(models.Model):
    pass



class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefgh12345')
    
    title = models.CharField(max_length=100, default='New vendor')
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    # description = models.TextField(null=True, blank=True, default='I am a vendor')
    description = RichTextUploadingField(null=True, blank=True, default='I am a vendor')

    address = models.CharField(max_length=100, default='Egypt, Cairo')
    contact = models.CharField(max_length=100, default='+20123456789')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'vendors'

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'%(self.image.url))
    
    def __str__(self):
        return self.title
PRODUCT_TYPE_CHOICES = (
    ('top_selling', 'Top Selling'),
    ('trending', 'Trending Products'),
    ('recent', 'Recently Added'),
    ('top_rated', 'Top Rated'),
    ('none', 'None'),  # للمنتجات اللي مش هتظهر في أي كاتيجوري خاص
)
    
class Product(models.Model):
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='none')
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='pro', alphabet='abcdefgh12345')
    available = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='product') 

    title = models.CharField(max_length=100, default='Fresh product')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    # description = models.TextField(null=True, blank=True, default='This is a product')
    description = RichTextUploadingField(null=True, blank=True, default='This is a product')


    price = models.DecimalField(max_digits=999999999,decimal_places=2, default="10.00")
    old_price = models.DecimalField(max_digits=999999999,decimal_places=2, default="20.00")
    
    specification = RichTextUploadingField(null=True, blank=True)
    # specification = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, default='Organic', null=True, blank=True)
    stock_count = models.CharField(max_length=100, default='10', null=True, blank=True)
    life = models.CharField(max_length=100, default='100 Days', null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    tags = TaggableManager(blank=True)

    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')


    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)
    
    def get_double_price(self):
        return self.price * 2
    class Meta:
        verbose_name_plural = 'products'

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'%(self.image.url))
    
    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product,related_name= "p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'
##############################################Cart , Order , OrederItems and Adress ##############
##############################################Cart , Order , OrederItems and Adress ##############
##############################################Cart , Order , OrederItems and Adress ##############
##############################################Cart , Order , OrederItems and Adress ##############


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999,decimal_places=2, default="10.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True) 
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='processing')

    class Meta:
        verbose_name_plural = 'Cart Order'



class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999999,decimal_places=2, default="10.00")
    total = models.DecimalField(max_digits=999999999,decimal_places=2, default="10.00")

    class Meta:
        verbose_name_plural = 'Cart Order Items'
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'%(self.image.url))
   

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>'%(self.image))
    

########################################Product Review  , Wishlist , Adress #####################    
########################################Product Review  , Wishlist , Adress #####################    
########################################Product Review  , Wishlist , Adress #####################    
########################################Product Review  , Wishlist , Adress #####################    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, default="Neutral")
    polarity = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating
    



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'