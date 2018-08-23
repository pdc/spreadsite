# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import include, path
import downblog.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path(r'resources/', include('spreadlinks.urls'), {'style_links': [], 'style_includes': ['spreadlinks.css', 'downblog/theme.css']}),
    path(r'', downblog.views.entry_list, {'root_dir': settings.DOWNBLOG_DIR}, 'blog-index'),
    path(r'admin/', admin.site.urls),
]
