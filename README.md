Spreadsheet-backed Website
==========================

Motivation
----------

This is a response to the frustration I had with a 'resource library' (list of
links) we were implementing for a quasi-governmental web site using a
content-management system (Drupal, as it happens). Our customer was actually the
subcontractor of the subcontractor of the quango charged with creating the site.
No-one in this hierarchy was capable of using the CMS to edit the links; instead
proposed changes floated up and down the layers of management in the form of a
spreadsheet with columns for title, keywords, and so on.

My job, as a programmer with over thirty years experience, was to copy the data
from the spreadsheet in to the web forms of the CMS. And to repeat the process
when they realized one of the links was wrong and sent us an updated
spreadsheet. And to repeat the process when deploying to the live web site once
the staging site had been signed off. 

At one point I had six spreadsheets. Three or four of them of them were named
Resource Library_21Nov2009_FINAL_rev2.xls, none of which was the 21 November
2009 release, and none of which was in any sense final.

Doing this by hand would have been tedious
and error-prone. I ended up concocting a Python program that read the links from
the spreadsheet, corrected the obvious typos in the URLs, and then called a web
service I added to the site to allow it to inject approproiate document nodes.
Once I had this working I was able to update the staging site, get them to sign
off the changes, and then make identical additions to the live site.

One of the biggest problems with this approach was the compelxity of the CMS.
All the features designed to allow the editors of the site to collaborate via
web forms were useless complications that got in the way of my automated
program. Why not, therefore, cut out the middleman, and have a web site that
runs directly from the spreadsheet?

Status
------

The present version is a proof of concept, using Django as its web framework. 

This is i no way a finely finished piece of work; I have not spent much more
than a working day's worth of work on it. If I were to seriously use this for a
site I would add a bit more finesse. I may work on it enough to get it in the
form of a re-usable Django app, just for the sake of the exercise.

How it Works
------------

A 'resource library' is a collection of links to resources on web sites (either
the same as this site or external sites). A library is defined by a directory
containing, at minimum, a spreadsheet with data about the links in it. Other,
optional, files may add more metadata to flesh out the definition.

Libraries are named after the directory. Libraries all live in a 'root
directory'. For the sample app, the root is `resource-libraries` and the Fan
films library is in `resource-libraries/fanfilms`.

The standard Drupal URLconf in `spreadlinks/urls.py` has these lines:
    
    urlpatterns = patterns('spreadsite.spreadlinks.views',
        (r'^$', 'library_list', {'root_dir': settings.SPREADLINKS_DIR}, 'library_list'),
        (r'^(?P<library_name>[^/]*)/$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
        (r'^(?P<library_name>[^/]*)/page(?P<page>[0-9]+)$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
        (r'^(?P<library_name>[^/]*)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
        (r'^(?P<library_name>[^/]*)/tags/(?P<urlencoded_keywords>[a-z_0-9+:-]+)/page(?P<page>[0-9]+)$', 'library_detail', {'root_dir': settings.SPREADLINKS_DIR}, 'library_detail'),
    )

Each view takes an argument that is the root directory; in this case it is in
turn acquired from the web site settings. The library name will match one of its
subdirectories. I recommend using short names consisting only of lowercase
letters and numbers; it keeps the URLs tidy.

Data Format
-----------

At present the spreadsheet must be in comma-separated values form; this is just
because I have not bothered adding support for one of the Exel-parsing libraries
available for Python. The first row MUST be column headings. Each of the
subsequent rows specifies an entry in the library.

The meaning of the columns is inferred from the column heading. Column headings
are normalized to lower case and spaces replaced with underscores before
interpreting them. The following columns are significant:

- `title`: The title of the link. Should be one line long and will be unique.
- `description`: A paragraph or two describing the link. Markdown format.
- `href` or `url`: The address of the resource being linked to.
- `keywords` or `main_keywords`: Keywords in the Main facet (see below)
- `FACET_keywords`: Keywords in an additional facet (where FACET is 
  replaced with the name of that facet).

At present other columns are ignored. (Probably they should be displayed as part
of the link descpription or something.)

Keywords are used to build a browseable drill-down navigation thingummy. 
The navigator automatically hides keywords that would lead to no matches.

A _facet_ is a collection of keywords that describe the resource in the same
way. You might use a secondary facet to
describe the resource type, or the intended audience, say. The navigator allows
the user to select keywords from separate facets independently.

The value of the keywords cells may contain multiple keywords. By default,
keywords are required to go one per line within the cell; this allows for
keywords to be normal phrases with spaces and punctuation.

Metadata
--------

Additional information about the library may be specified with a separate file
`METADATA.txt`. This contains one or more headings following the RFC-2822 format
of heading:value, followed by a blank line and then the description of the
library. The description uses Markdown format.

The following headers are understood:

- `Title`: A title for the library as a whole.
- `Keyword-Separator`: A character to use instead of newlines to separate
keywords in the data file.

If there is no `METADATA.txt`, or no title is specified, then it uses library name
(the same as the directiory name). 


    




