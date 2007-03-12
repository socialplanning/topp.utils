"""
functions related to urls: 
parsing, etc. [just parsing for now]
"""

import re

### functions for uri parsing

relative_uri_re = r'(?:[a-z0-9\-]+|[a-z0-9][a-z0-9\-\.\_]*\.[a-z]+)' + r'(?::[0-9]+)?' + r'(?:/.*)?$'

def uri_re_string(scheme=('http','https')):
    """ returns a regular expression pattern for matching uris """

    if scheme:
        if not isinstance(scheme, basestring):
            scheme = r'(' + r'|'.join(scheme) + r')'
        scheme += r'://'
    else:
        scheme = r''        
    return ( r'^' + scheme +  relative_uri_re )

url_re = re.compile(uri_re_string(), re.I)

def is_url(string):
    """ indicates if the given string is legitimate url syntax """
    if re.match(url_re, string):
        return True
    return False

def uri_type(string):
    
    uri_types = {'http': uri_re_string('http'),
                 'https': uri_re_string('https'),
                 'ftp': uri_re_string('ftp'),
                 'file': r'^file:///' + relative_uri_re,
                 }

    for i in uri_types:
        if re.match(uri_types[i], string):
            return i
