# Encoding: UTF-8
# Create your views here.
import re
import datetime
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
from spreadlinks.models import get_library_or_404
from downblog.models import get_entry_list


def entry_list(request, root_dir):

    entries = get_entry_list(root_dir)
    entry = entries[-1]

    template_args = {
        'entry': entry,
    }

    # Let’s add some links from a resource library.
    lib = get_library_or_404(settings.SPREADLINKS_DIR, 'spreadsite')
    links = lib.all_links
    template_args['links'] = links

    return render(request, 'downblog/entry_list.html', template_args)

