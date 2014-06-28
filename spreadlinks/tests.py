# Encoding: UTF-8
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from __future__ import unicode_literals
from django.test import TestCase
import os
import shutil
from django.utils import safestring
from linklibrarylib import *

class SimpleTest(TestCase):
    dir_name = 'test-resources'

    def setUp(self):
        if os.path.exists(self.dir_name):
            shutil.rmtree(self.dir_name)
        os.mkdir(self.dir_name)

    def test_tagify(self):
        self.assertEqual('hello', tagify('hello'))
        self.assertEqual('cat-socks', tagify('Cat socks'))

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

    def test_library_list_zero(self):
        libs = LibrarySet(self.dir_name)
        self.assertEqual(0, len(libs))

    def test_library_list_one(self):
        os.mkdir(os.path.join(self.dir_name, 'foo'))
        with open(os.path.join(self.dir_name, 'foo/METADATA.txt'), 'wt') as output:
            output.write('Title: Fabulous Object Organization\nBoo: Ba\n\nHello, world.\nPleased to be here')

        libs = LibrarySet(self.dir_name)
        self.assertEqual(1, len(libs))
        lib = libs['foo']
        self.assertEqual('Fabulous Object Organization', lib.title)
        self.assertEqual('Hello, world.\nPleased to be here', lib.description)
        self.assertEqual('Ba', lib.boo)
        self.assertEqual('foo', lib.name)

    def test_library_sans_metadata(self):
        os.mkdir(os.path.join(self.dir_name, 'bar'))

        libs = LibrarySet(self.dir_name)
        self.assertEqual(1, len(libs))
        lib = libs['bar']
        self.assertEqual('Bar', lib.title)
        self.assertEqual('', lib.description)
        self.assertEqual('bar', lib.name)

    def test_simple_links(self):
        os.mkdir(os.path.join(self.dir_name, 'baz'))
        with open(os.path.join(self.dir_name, 'baz/data.csv'), 'wt') as output:
            output.write('Title,Description,Keywords,URL\nCrumbs,Crummy,cake,http://example.org/\nSlime,Slimy,goo,http://example.com/')

        libs = LibrarySet(self.dir_name)
        lib = libs['baz']
        self.assertEqual(2, len(lib.all_links))
        self.check_link(lib.all_links[0], 'Crumbs', 'http://example.org/', 'Crummy', ['cake'])
        self.check_link(lib.all_links[1], 'Slime', 'http://example.com/', 'Slimy', ['goo'])

    def test_skip_blank_lines(self):
        os.mkdir(os.path.join(self.dir_name, 'baz'))
        with open(os.path.join(self.dir_name, 'baz/data.csv'), 'wt') as output:
            output.write('Title,Description,Keywords,URL,,,\nCrumbs,Crummy,cake,http://example.org/,,,\nSlime,Slimy,goo,http://example.com/,,,\n,,,,,,,,,\n,,,,,,,,\n')

        libs = LibrarySet(self.dir_name)
        lib = libs['baz']
        self.assertEqual(2, len(lib.all_links))
        self.check_link(lib.all_links[0], 'Crumbs', 'http://example.org/', 'Crummy', ['cake'])
        self.check_link(lib.all_links[1], 'Slime', 'http://example.com/', 'Slimy', ['goo'])

    def check_link(self, link, title, href, description, keywords):
        self.assertEqual(title, link.title)
        self.assertEqual(href, link.href)
        self.assertEqual(description, link.description)

    def test_tagging(self):
        os.mkdir(os.path.join(self.dir_name, 'quux'))
        with open(os.path.join(self.dir_name, 'quux/data.csv'), 'wt') as output:
            output.write('Title,Description,Keywords,URL\nCrumbs,Crummy,cake,http://example.org/\nSlime,Slimy,goo,http://example.com/\nSlimy crumbs,Slimy and crumby,cake goo,http://example.net/')

        lib = LibrarySet(self.dir_name)['quux']
        self.assertEqual(set(['cake', 'goo']), lib.main_keywords)
        self.assertEqual(3, len(lib.all_links))

        cake_links = lib.filtered_links(['cake'])
        self.assertEqual(2, len(cake_links))
        self.assertEqual('Crumbs', list(cake_links)[0].title)
        self.assertEqual('Slimy crumbs', list(cake_links)[1].title)

        # Equivalewnt to invoking with the special facet named ‘main’
        cake_links = lib.filtered_links({'main': ['cake']})
        self.assertEqual(2, len(cake_links))
        self.assertEqual('Crumbs', list(cake_links)[0].title)
        self.assertEqual('Slimy crumbs', list(cake_links)[1].title)

        goo_links = lib.filtered_links(['goo'])
        self.assertEqual(2, len(goo_links))
        self.assertEqual('Slime', list(goo_links)[0].title)
        self.assertEqual('Slimy crumbs', list(goo_links)[1].title)

        cake_goo_links = lib.filtered_links(['cake', 'goo'])
        self.assertEqual(1, len(cake_goo_links))
        self.assertEqual('Slimy crumbs', list(cake_goo_links)[0].title)

        self.assertEqual('', lib.urlencode_keywords([]))
        self.assertEqual('cake', lib.urlencode_keywords({'main': ['cake']}))
        self.assertEqual('cake+goo', lib.urlencode_keywords({'main': ['goo', 'cake']}))

        self.assertEqual(set(['cake']), lib.urldecode_keywords('cake')['main'])
        self.assertEqual(set(['cake', 'goo']), lib.urldecode_keywords('cake+goo')['main'])
        self.assertEqual({'main': set()}, lib.urldecode_keywords(''))

    def test_separator(self):
        os.mkdir(os.path.join(self.dir_name, 'quux2'))
        with open(os.path.join(self.dir_name, 'quux2/METADATA.txt'), 'wt') as output:
            output.write('Title: Quantum Uniform Ungulate Xerography 2\nkeyword-separator: ;\nBoo: Ba\n\nHello, world.\nPleased to be here')

        with open(os.path.join(self.dir_name, 'quux2/data.csv'), 'wt') as output:
            output.write('Title,Description,Keywords,URL\nCrumbs,Crummy,cake;socks,http://example.org/\nSlime,Slimy,goo; hose,http://example.com/\nSlimy crumbs,Slimy and crumby, cake; goo ,http://example.net/')

        lib = LibrarySet(self.dir_name)['quux2']
        self.assertEqual(set(['cake', 'goo', 'hose', 'socks']), lib.main_keywords)
        link = lib.all_links[0]
        self.assertEqual(set(['cake', 'socks']), link.main_keywords)

        link = lib.all_links[1]
        self.assertEqual(set(['goo', 'hose']), link.main_keywords)

        link = lib.all_links[2]
        self.assertEqual(set(['cake', 'goo']), link.main_keywords)

    def test_other_keywords(self):
        os.mkdir(os.path.join(self.dir_name, 'zub'))
        with open(os.path.join(self.dir_name, 'zub/data.csv'), 'wt') as output:
            output.write('Title,Keywords,Colour keywords,URL\nHarlequin,cat,black white,http://www.flickr.com/photos/jeremy_dennis/4217338130/\nTeasel,cat,black,http://www.flickr.com/photos/jeremy_dennis/3713607489/')

        lib = LibrarySet(self.dir_name)['zub']
        link = lib.all_links[0]
        self.assertEqual(set(['black', 'white']), link.facet_keywords['colour'])
        self.assertEqual(set(['cat']), link.facet_keywords['main'])
        link = lib.all_links[1]
        self.assertEqual(set(['black']), link.facet_keywords['colour'])
        self.assertEqual(set(['cat']), link.facet_keywords['main'])

        self.assertEqual(1, len(lib.filtered_links({'colour': set(['white'])})))
        self.assertEqual(2, len(lib.filtered_links({'colour': set(['black'])})))

        self.assertEqual('cat+colour:black+colour:white', lib.urlencode_keywords(
            {'colour': ['black', 'white'], 'main': ['cat']}))
        self.assertEqual({'colour': set(['black', 'white']), 'main': set(['cat'])},
            lib.urldecode_keywords('cat+colour:black+colour:white'))


    def test_formatted_properties(self):
        os.mkdir(os.path.join(self.dir_name, 'baz'))
        with open(os.path.join(self.dir_name, 'baz/data.csv'), 'wt') as output:
            output.write(b'Title,Description,Keywords,URL\nCrumbs,Crummy,cake,http://example.org/\nSlime,"Slimy\n\n‘Wormy’",goo,http://example.com/')

        libs = LibrarySet(self.dir_name)
        lib = libs['baz']
        self.assertEqual(2, len(lib.all_links))
        self.assertHTMLEqual('<p>Crummy</p>', lib.all_links[0].description_formatted)
        self.assertHTMLEqual('<p>Slimy</p><p>‘Wormy’</p>', lib.all_links[1].description_formatted)
        self.assertTrue(isinstance(lib.all_links[0].description_formatted, safestring.SafeText))
