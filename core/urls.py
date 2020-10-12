from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('Profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('Profile/', profile, name='profile'),
    path('Boutiques/', boutiks, name='boutiks'),
    path('My/Boutiques', myboutiks, name="myboutiks"),
    path('My/Produits/', myproducts, name="myprods"),
    path('Ajouter/boutiques/', AddBoutikView.as_view(), name='addboutiks'),
    url(r'^Boutik/(?P<pk>[0-9]+)/update/$', BoutikUpdateView.as_view(), name='boutiks_update'),
    url(r'^Boutik/(?P<pk>[0-9]+)/delete/$', BoutikDeleteView.as_view(), name='boutiks_delete'),
     path('Ajouter/Produits/', AddProductView.as_view(), name='addproducts'),
    url(r'^Product/(?P<pk>[0-9]+)/update/$', ProductUpdateView.as_view(), name='products_update'),
    url(r'^Product/(?P<pk>[0-9]+)/delete/$', ProductDeleteView.as_view(), name='products_delete'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<boutik>[-\w]+)/$', boutik_detail, name='boutik_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<itemse>[-\w]+)/seller/$', itemse_detail, name='itemse_detail'),
    path('About/', about, name='about'),
    path('Contact/', contact, name='contact'),
    path('Aide/', aide, name="aide"),
    path('Shop/', shop, name='shop'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('order-view/', order_view, name='order-view'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment-S/stripe/', PaymentView.as_view(), name='payment_cc'),
    path('payment-P/paypal/', payment_paypal, name='payment_paypal'),
    path('payment-P/Done/', payment_p_done, name='payment_p_done'),
    path('payment-P/Annuler/', payment_p_canceled, name='payment_p_canceled'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
