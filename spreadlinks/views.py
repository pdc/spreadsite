# Create your views here.

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
import datetime
from spreadsite.spreadlinks.linklibrarylib import *
from spreadsite.spreadlinks.models import *

def render_with_template(default_template_name, default_base_template_name='spreadlinks/base.html'):
    """Decorator to wrap template-based rendering around a view function returning template variables."""
    def decorator(func):
        def wrapped_handler(request, template_name=None, base_template_name=None, *args, **kwargs):
            result = func(request, *args, **kwargs)
            if isinstance(result, HttpResponse):
                return result
            if not result.get('base_template_name'):
                result['base_template_name'] = base_template_name or default_base_template_name
            return render_to_response(template_name or default_template_name, result, RequestContext(request))
        return wrapped_handler
    return decorator
    
    
@render_with_template('spreadlinks/library-list.html')
def library_list(request, root_dir):
    return {
        'libraries': sorted(get_library_set(root_dir).values()),
    }

@render_with_template('spreadlinks/library-detail.html')
def library_detail(request, root_dir, library_name, urlencoded_keywords='', page=1):
    lib = get_library_or_404(root_dir, library_name)
    facet_keywords = lib.urldecode_keywords(urlencoded_keywords)
    links = lib.filtered_links(facet_keywords) if facet_keywords else lib.all_links
    facet_drillupdowns = {}
    for facet_name, keywords in facet_keywords.items():
        drilldowns = []
        for k in lib.facet_keywords[facet_name] - keywords:
            more_keywords = dict((facet_name, set(keywords)) for (facet_name, keywords) in facet_keywords.items())
            more_keywords[facet_name] |= set([k])
            fewer_links = lib.filtered_links(more_keywords)
            if fewer_links:
                drilldowns.append({
                    'keyword': k,
                    'urlencoded': lib.urlencode_keywords(more_keywords),
                    'links': fewer_links,
                    'link_count': len(fewer_links),
                })
        drillups = []
        for k in keywords:
            fewer_keywords = dict((facet_name, set(keywords)) for (facet_name, keywords) in facet_keywords.items())
            fewer_keywords[facet_name].discard(k)
            more_links = lib.filtered_links(fewer_keywords)
            drillups.append({
                'keyword': k,
                'urlencoded': lib.urlencode_keywords(fewer_keywords),
                'links': more_links,
                'link_count': len(more_links),
            })
        facet_drillupdowns[facet_name] = {'drillups': drillups, 'drilldowns': drilldowns}
        
    facet_drillupdowns = sorted(facet_drillupdowns.items(),
        key=lambda (facet_name, facet): (facet_name != 'main', facet_name))
        
    # Now the machinery for paging thbrough long lists of links.    
    paginator = Paginator(links, settings.SPREADLINKS_PER_PAGE)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    try:
        links_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        links_page = paginator.page(paginator.num_pages)
        
    # Calculate the URLs for the previous and next links, if any.
    kwargs = {'library_name': library_name}
    if urlencoded_keywords: 
        kwargs['urlencoded_keywords'] = urlencoded_keywords
    if links_page.has_previous():
        if links_page.previous_page_number() > 1:
            kwargs['page'] = str(links_page.previous_page_number())
        
        prev_href = reverse('library_detail', kwargs=kwargs)
    else:
        prev_href = None
    if links_page.has_next():
        kwargs = {'library_name': library_name}
        if urlencoded_keywords: 
            kwargs['urlencoded_keywords'] = urlencoded_keywords
        kwargs['page'] = str(links_page.next_page_number())
        next_href = reverse('library_detail', kwargs=kwargs)
    else:
        next_href = None
        
    return {
        'library': lib, 
        'base_template_name': lib.base_template if hasattr(lib, 'base_template') else None,
        'links': links_page,
        'link_count': len(links),
        'prev_href': prev_href,
        'next_href': next_href,
        'facet_keywords': facet_keywords,
        'urlencoded_keywords': urlencoded_keywords,
        'facet_drillupdowns': facet_drillupdowns,
    }

