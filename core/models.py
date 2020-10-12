from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from autoslug import AutoSlugField

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biographie = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    # address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)
    facebook = models.CharField(max_length=200, help_text="example: https://facebook.web/{username}/", null=True, blank=True)
    whatsapp = models.CharField(max_length=200, help_text="example: +50943208550", null=True, blank=True)
    instagram = models.CharField(max_length=200, help_text="example: https://instagram.com/{username}/", null=True, blank=True)
    photo = models.ImageField(default='photo.jpg', upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
class Contactus(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name_plural = "Contactus"
 
    def __str__(self):
        return self.name + "-" +  self.email
    


CATEGORY_CHOICES = (
    ('SB', 'Shirts And Blouses'),
    ('TS', 'T-Shirts'),
    ('SK', 'Skirts'),
    ('HS', 'Hoodies&Sweatshirts')
)

LABEL_CHOICES = (
    ('S', 'vente'),
    ('N', 'Nouveau'),
    ('P', 'promotion')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


# class Slide(models.Model):
#     caption1 = models.CharField(max_length=100)
#     caption2 = models.CharField(max_length=100)
#     link = models.CharField(max_length=100)
#     image = models.ImageField(help_text="Size: 1920x570")
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return "{} - {}".format(self.caption1, self.caption2)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

LABEL_CHOICES_BOUTIQUE = (
    ('O', 'ouvert'),
    ('F', 'fermer')
)

TYPE_CHOICES_BOUTIQUE = (
    ('MG', 'Magasin'),
    ('MK', 'Market'),
    ('SP', 'Shop'),
    ('AG', 'Agence'),
    ('PA', 'Produit Alimentaire'),
    ('PC', 'Produit Cosmetique'),
    ('MS', 'Multi-Service'),
    ('RR', 'Restaurant'),
    ('GG', 'Garage'),
    ('MM', 'Multi-Media'),
    ('QC', 'Quincallerie'),
    ('HT', 'Hotel'),
    ('VH', 'Vehicule'),
)
# from django.contrib.auth.models import User
class Local(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to='local/img/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

class Boutique(models.Model):
    name = models.CharField(max_length=250)
    localite = models.ForeignKey(Local, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES_BOUTIQUE, max_length=1)
    type_boutique = models.CharField(choices=TYPE_CHOICES_BOUTIQUE, max_length=2)
    image = models.FileField(upload_to='boutik/img/', blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique_with=['name'], unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               related_name='boutik_auth', on_delete=models.CASCADE)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_on',)
    
    def __str__(self):
        return self.name
    
    def type(self):
        return self.get_type_boutique_display()

    def get_absolute_url(self):
        return reverse('core:boutik_detail',args=[self.created_on.year,self.created_on.strftime('%m'),self.created_on.strftime('%d'),self.slug])

LABEL_CHOICES_SELLERS = (
    ('V', 'vente'),
    ('N', 'nouveau'),
    ('P', 'promotion')
)

CATEGORY_CHOICES_SELLERS = (
    ('CC', 'Chemises et chemisiers'),
    ('TS', 'T-Shirts'),
    ('JP', 'Jupes'),
    ('SS', 'Sweats à capuche et sweat-shirts')
)

STOCK_CHOICES_SELLER = (
    ('D', 'Disponible'),
    ('I', 'Indisponible'),
    ('P', 'Presque-terminé')
)

LIVRAISON_CHOICES_SELLER = (
    ('I', 'Inclus'),
    ('P', 'Pas-Inclus')
)

SIZE_CHOICES_SELLER = (
    ('M', 'Medium'),
    ('L', 'Large'),
    ('SL', 'Longueur standard'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large')
)

ETATS_CHOICES_SELLER = (
    ('N', 'Neuf'),
    ('U', 'Usage')
)

class ItemSeller(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               related_name='item_auth', on_delete=models.CASCADE)
    boutique = models.ForeignKey(Boutique, related_name='items', on_delete=models.CASCADE)
    # size = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    etat = models.CharField(choices=ETATS_CHOICES_SELLER, max_length=1)
    label = models.CharField(choices=LABEL_CHOICES_SELLERS, max_length=1)
    livraison = models.CharField(choices=LIVRAISON_CHOICES_SELLER, max_length=1)
    size = models.CharField(choices=SIZE_CHOICES_SELLER, max_length=3)
    categories = models.CharField(choices=CATEGORY_CHOICES_SELLERS, max_length=2)
    slug = AutoSlugField(populate_from='title',
                         unique_with=['title'], unique=True)
    stock = models.CharField(choices=STOCK_CHOICES_SELLER, max_length=1)
    description_court = models.CharField(max_length=50)
    description_long = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='product_photos/%Y/%m/%d/')
    photo_2 = models.ImageField(
        upload_to='product_photos/%Y/%m/%d/', blank=True, null=True)
    photo_3 = models.ImageField(
        upload_to='product_photos/%Y/%m/%d/', blank=True, null=True)
    photo_4 = models.ImageField(
        upload_to='product_photos/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{} disponible dans {}'.format(self.title, self.boutique)

    def category(self):
        return self.get_categories_display()
    
    def get_absolute_url(self):
        return reverse('core:itemse_detail',args=[self.created.year,self.created.strftime('%m'),self.created.strftime('%d'),self.slug])

STOCK_CHOICES = (
    ('D', 'Disponible'),
    ('I', 'Indisponible'),
    ('P', 'Presque-terminé')
)

LABEL_CHOICES = (
    ('V', 'vente'),
    ('N', 'nouveau'),
    ('P', 'promotion')
)

LIVRAISON_CHOICES = (
    ('I', 'Inclus'),
    ('P', 'Pas-Inclus')
)

SIZE_CHOICES_SELLER = (
    ('M', 'Medium'),
    ('L', 'Large'),
    ('SL', 'Longueur standard'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large')
)

ETATS_CHOICES = (
    ('N', 'Neuf'),
    ('U', 'Usage')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    # size = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    etat = models.CharField(choices=ETATS_CHOICES, max_length=1)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    livraison = models.CharField(choices=LIVRAISON_CHOICES, max_length=1)
    size = models.CharField(choices=SIZE_CHOICES_SELLER, max_length=3)
    slug = models.SlugField()
    stock = models.CharField(choices=STOCK_CHOICES_SELLER, max_length=1)
    description_court = models.CharField(max_length=50)
    description_long = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='product_photos/%Y/%m/%d/')
    photo_2 = models.ImageField(
        upload_to='product_photos/%Y/%m/%d/', blank=True, null=True)
    photo_3 = models.ImageField(
        upload_to='product_photos/%Y/%m/%d/', blank=True, null=True)
    photo_4 = models.ImageField(
        upload_to='product_photos/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title
    
    def get_item_price(self):
        return self.price

    def get_discount_item_price(self):
        return self.discount_price

    def get_amount_saved(self):
        return self.get_item_price() - self.get_discount_item_price()

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'BillingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    quartier_addresse = models.CharField(max_length=100)
    apartment_addresse = models.CharField(max_length=100)
    pays = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
