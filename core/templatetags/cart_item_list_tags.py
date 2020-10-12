from django import template
from django.utils.safestring import mark_safe

from core.models import Order

register = template.Library()

@register.filter
def cart_item(user):
    if user.is_authenticated:
        items = Order.objects.filter(user=user, ordered=False)
        if items.exists():
            items_li = ""
            for i in items:
                items_li += """<li><div class="wrap"><div class="image"><img src="/media/{}" alt=""></div><div class="caption"><span class="comp-header st-1 text-uppercase">{}<span>{}</span></span><span class="price"><span class="text-grey-dark">$</span> <del>{}</del> ${}</span></div><a href="/remove-from-cart/{}" class="remove-btn bg-blue"><i class="icofont icofont-bucket"></i></a></div></li>""".format(i.item.image, i.item.title, i.item.category, i.item.price, i.item.discount_price, i.item.slug)
            return mark_safe(items_li)