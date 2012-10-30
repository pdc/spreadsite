from django.db import models
from django.core.cache import cache
from django.http import Http404
from spreadlinks.linklibrarylib import *

def get_library_set(root_dir):
    """Find the libraries in the specified file-system directoiry."""
    key = 'library_set'
    result = cache.get(key)
    if not result:
        result = LibrarySet(root_dir)
        cache.set(key, result)
    return result

def get_library_or_404(root_dir, library_name):
    """Given a parent direcgtory and library name, find the library or throw an HTTP exception."""
    try:
        return get_library_set(root_dir)[library_name]
    except KeyError, e:
        raise Http404()


# Create your models here.
