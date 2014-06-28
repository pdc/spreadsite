# Map URLs to functions for the spreadlinks module.

from django.conf.urls import url
from django.conf import settings
import spreadlinks.views


urlpatterns = [
    url(r'^$', spreadlinks.views.library_list, {'root_dir': settings.SPREADLINKS_DIR}, 'library_list'),
    url(r'^(?P<library_name>[^/]*)/$', spreadlinks.views.library_detail, {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    url(r'^(?P<library_name>[^/]*)/page(?P<page>[0-9]+)$', spreadlinks.views.library_detail, {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    url(r'^(?P<library_name>[^/]*)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)$', spreadlinks.views.library_detail, {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    url(r'^(?P<library_name>[^/]*)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)/page(?P<page>[0-9]+)$', spreadlinks.views.library_detail, {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
]