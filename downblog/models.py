# -*- coding: utf-8 -*-


import os
import re
from datetime import datetime
import email.parser
from markdown import Markdown
from collections import namedtuple
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe


# Date followed by slug.
entry_file_name_re = re.compile(r'^(199[0-9]|20[0-9][0-9])-([0-1][0-9])-([0-3][0-9])[._-]?([a-zA-Z0-9-]*)\.(e|md)$')


parser = email.parser.Parser()

formatter = Markdown()

class Entry(namedtuple('Entry', ['y', 'm', 'd', 'slug', 'suffix', 'dir_name', 'file_name'])):
    """One entry in the blog."""

    @cached_property
    def msg(self):
        """Return an RFC 2822 parsed message instance"""
        with open(os.path.join(self.dir_name, self.file_name), 'r') as strm:
            return parser.parse(strm)

    @cached_property
    def body(self):
        return self.msg.get_payload()

    def body_formatted(self):
        return mark_safe(formatter.convert(self.body))

    def title(self):
        return self.msg['title']

    def published(self):
        return datetime(int(self.y), int(self.m, 10), int(self.d, 10), 12, 0, 0)


def get_entry_list(root_dir):
    """Get list of Entry instances."""
    entries = []
    for dir_name, subdirs, files in os.walk(root_dir):
        for file_name in files:
            m = entry_file_name_re.match(file_name)
            if m:
                entries.append(Entry._make(m.groups() + (dir_name, file_name)))
    entries.sort() # Most recent last.
    return entries
