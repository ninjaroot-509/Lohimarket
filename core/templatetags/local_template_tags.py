from django import template
from django.utils.safestring import mark_safe

from core.models import Local

register = template.Library()


@register.simple_tag
def localites():
    items = Local.objects.filter(is_active=True).order_by('name')
    items_li = ""
    for i in items:
        items_li += """<li><a href="/local/{}">{}</a></li>""".format(i.slug, i.name)
    return mark_safe(items_li)
