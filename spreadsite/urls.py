# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
import downblog.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^resources/', include('spreadlinks.urls')),

    url(r'^$', downblog.views.entry_list, {'root_dir': settings.DOWNBLOG_DIR}, 'blog-index'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
