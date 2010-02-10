#!/usr/bin/env python
# encoding: utf-8
"""
linklibrarylib.py

Created by Damian Cugley on 2010-01-01.
Copyright (c) 2010 Damian Cugley. All rights reserved.
"""

import sys
import os
import UserDict
import email # RFC 2822 parsing
import csv 

MAIN = 'main'

class Error(Exception):
    """Base class for exceptions in this module."""
    pass
    
    
class ReadOnlyError(Error):
    """Can't be written to."""
    def __init__(self, thing, msg=None):
        self.msg = msg or u'Cannot write to %s' % thing
        self.thing = thing
        
        
def tagify(*args):
    """Generate a (hierarchical) tag from a name.
    
    Generally a single argument is passed, the keyword to convert to a tag.
    If two args are passed, the first specifies a namespace and the second the keyword.
    The resulting tag uses prefix notation, in the style namespace:keyword .
    The special namespace MAIN is never used as a prefix.
    """
    if args[0] == MAIN:
        args = args[1:]
    return '-'.join(':'.join(args).lower().replace('_', '-').split())

class LibrarySet(UserDict.DictMixin):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        
    def load_libraries(self):
        self._libraries = {}
        for file_name in os.listdir(self.root_dir):
            full_name = os.path.join(self.root_dir, file_name)
            if os.path.isdir(full_name):
                self._libraries[file_name] = Library(file_name, full_name)   
            
    def __unicode__(self):
        return '<library root_dir=%s>' % self.root_dir     
        
    def __getitem__(self, key):
        if not hasattr(self, '_libraries'):
            self.load_libraries()
        return self._libraries[key]
        
    def __setitem__(self, key, val):
        raise ReadOnlyError(self) 
    
    def __delitem__(self, key):
        raise ReadOnlyError(self) 
        
    def keys(self):
        if not hasattr(self, '_libraries'):
            self.load_libraries()
        return self._libraries.keys()
        
class Library(object):
    keyword_separator = None # May be overidden in instances.
    
    def __init__(self, name, dir_name):
        self.name = name
        self.dir = dir_name
        metadata_name = os.path.join(dir_name, 'METADATA.txt')
        if os.path.exists(metadata_name):
            with open(metadata_name, 'rb') as stream:
                metadata = email.message_from_file(stream)
            self.description = metadata.get_payload()
            for key, value in metadata.items():
                setattr(self, tagify(key).replace('-', '_'), value)
        else:
            self.title = name.title()
            self.description = ''
            
        # Scan the directory for data files.
        self.all_links = []
        for file_name in os.listdir(dir_name):
            if file_name.endswith('.csv'):
                with open(os.path.join(dir_name, file_name), 'rb') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for d in reader:
                        if any(k and v for (k, v) in d.items()):
                            self.all_links.append(Link(self, d))
                            
        # Prepare for indexing by keyword.
        self.facet_keywords = {'main': set()}
        for link in self.all_links:
            for facet_name, keywords in link.facet_keywords.items():
                self.facet_keywords.setdefault(facet_name, set()).update(keywords)
        self.main_keywords = self.facet_keywords[MAIN]
        self.facet_keywords_by_tag = dict((tagify(f, k), (f, k)) for (f, keywords) in self.facet_keywords.items() for k in keywords)
        
    def filtered_links(self, keywords):
        return list(self.filtered_links_iter(self.all_links, keywords))
        
    def filtered_links_iter(self, links, facet_keywords):
        if isinstance(facet_keywords, set):
            facet_keywords = {MAIN: facet_keywords}
        elif isinstance(facet_keywords, list):
            facet_keywords = {MAIN: set(facet_keywords)}
        for link in links:
            if all(set(keywords).issubset(link.facet_keywords[facet_name]) 
                    for (facet_name, keywords) in facet_keywords.items()):
                yield link
                
    def urlencode_keywords(self, facet_keywords):
        if isinstance(facet_keywords, list) or isinstance(facet_keywords, set):
            # As a special case, we project this list of keywords in to the ‘main’ facet
            tags = sorted(tagify(k) for k in facet_keywords)
        else:
            tags = []
            for facet_name, keywords in facet_keywords.items():
                more_tags = sorted(tagify(facet_name, k) for k in keywords)
                if facet_name == MAIN:
                    tags = more_tags + tags
                else:
                    tags = tags + more_tags
        return '+'.join(tags)
        
    def urldecode_keywords(self, urlencoded_keywords):
        result = dict((facet_name, set()) for facet_name in self.facet_keywords.keys())
        if not urlencoded_keywords: 
            return result
        for tag in urlencoded_keywords.split('+'):
            try:
                facet_name, keyword = self.facet_keywords_by_tag[tag]
            except KeyError, e:
                print self.facet_keywords
                return None
            result[facet_name].add(keyword)
        return result
        
                        
class Link(object):
    def __init__(self, library, atts):
        self.facet_keywords = {}
        sep = library.keyword_separator
        for key0, val in atts.items():
            if not key0:
                continue
            key = tagify(key0)
            if key.endswith('keywords'):
                val = set(k.strip() for k in val.split(sep))
                if key == 'keywords':
                    key = 'main_keywords'
                    facet_name = MAIN
                else:
                    facet_name = key0[:-9]
                self.facet_keywords[facet_name] = val
            elif key == 'url':
                key = 'href'
            setattr(self, key, val)