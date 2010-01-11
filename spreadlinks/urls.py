# Map URLs to functions for the spreadlinks module.

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('spreadsite.spreadlinks.views',
    (r'^$', 'library_list', {'root_dir': settings.SPREADLINKS_DIR}, 'library_list'),
    (r'^(?P<library_name>[^/]*)/$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    (r'^(?P<library_name>[^/]*)/page(?P<page>[0-9]+)$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    (r'^(?P<library_name>[^/]*)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    (r'^(?P<library_name>[^/]*)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)/page(?P<page>[0-9]+)$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
)
