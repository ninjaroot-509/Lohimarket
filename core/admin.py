from django.contrib import admin

from .models import *


# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Mettre à jour les commandes de remboursement accordées'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['user',
                   'ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'quartier_addresse',
        'apartment_addresse',
        'pays',
        'zip',
        'city',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'pays']
    search_fields = ['user', 'quartier_addresse', 'apartment_addresse', 'city', 'zip']


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
    ]
    list_filter = ['title', 'category']
    search_fields = ['title', 'category']
    prepopulated_fields = {"slug": ("title",)}
    actions = [copy_items]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active'
    ]
    list_filter = ['title', 'is_active']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)

class ItemSellerAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
    ]
    list_filter = ['title', 'price']
    search_fields = ['title', 'price']
    prepopulated_fields = {"slug": ("title",)}
    actions = [copy_items]

class LocalAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
        'slug'
    ]
    list_filter = ['name',]
    search_fields = ['name',]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ItemSeller, ItemSellerAdmin)
admin.site.register(Local, LocalAdmin)

admin.site.register(OrderItem)
# admin.site.register(ItemSeller)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Boutique)
admin.site.register(BillingAddress, AddressAdmin)

class ContactusAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'

admin.site.register(Contactus, ContactusAdmin)
admin.site.register(Profile)