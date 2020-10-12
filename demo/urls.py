from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

# Ici les urls pour les pages qu'on ne veux pas traduire
# urlpatterns = [
#     url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
#         home_files, name='home-files'),
# ]

# On ajoute dans i18n_patterns la liste des urls des pages a traduire 
urlpatterns = i18n_patterns(
    path('', include('core.urls', namespace='core')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('accounts/', include('allauth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    path('admin/', admin.site.urls)
)

# confidentials
# conditions
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
