# Create your views here.
import os
import re
import email.parser
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from spreadsite.spreadlinks.models import get_library_or_404

# Date followed by slug.
entry_file_name_re = re.compile(r'^(199[0-9]|20[0-9][0-9])-([0-1][0-9])-([0-3][0-9])[._-]?([a-zA-Z0-9-]*)\.(e|md)$')

parser = email.parser.Parser()

def entry_list(request, root_dir):
    # Get list of entries
    # TODO. Split in to separate function.
    # TODO. Cache
    entries = []
    for dir_name, subdirs, files in os.walk(root_dir):
        for file_name in files:
            m = entry_file_name_re.match(file_name)
            if m:
                entries.append(m.groups() + (dir_name, file_name))
    entries.sort() # Most recent last.
    
    lib = get_library_or_404(settings.SPREADLINKS_DIR, 'spreadsite')
    links = lib.all_links
    
    entry = entries[-1]
    y, m, d, slug, suffix, dir_name, file_name = entry
    with open(os.path.join(dir_name, file_name), 'rb') as input:
        msg = parser.parse(input)
    template_args = {
        'title': msg['title'],
        'body': msg.get_payload(),
        'links': links,
    }        
    
    return render_to_response('downblog/entry_list.html', template_args, RequestContext(request))
        
