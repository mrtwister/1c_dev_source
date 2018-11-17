#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Роман Беляев'
SITENAME = 'developer 1C'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Vladivostok'

DEFAULT_LANG = 'Russian'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "themes/myTheme"

STATIC_PATHS = ['extra']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},
                       'extra/favicon.ico': {'path': 'favicon.ico'},}

# PLUGIN_PATHS = ['pelican-plugins']
# #PLUGINS = ['read_more_link']

# # This settings indicates that you want to create summary at a certain length
# SUMMARY_MAX_LENGTH = 500

# #This indicates what goes inside the read more link
# READ_MORE_LINK = '<span>continue</span>'

# # This is the format of the read more link
# READ_MORE_LINK_FORMAT = '<a class="read-more" href="{{ SITEURL }}/{{ article.url }}">Читать далее --></a>'
