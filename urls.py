from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^spreadsite/', include('spreadsite.foo.urls')),
    (r'^resources/', include('spreadsite.spreadlinks.urls')),
    
    (r'^$', 'spreadsite.downblog.views.entry_list', {'root_dir': settings.DOWNBLOG_DIR}, 'blog-index'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)
