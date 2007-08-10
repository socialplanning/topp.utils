#!/usr/bin/env python

"""
remove tags from html
"""

import re
regexes = ('<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)>', 
           '<(?:([^>"]*?)|(?:"[^"]*"))*>',
           '&[A-Za-z#0-9]+;', 
           '<')
regexes = [ re.compile(i,re.S) for i in regexes ]

def detag(string):
    """
    remove all tags from HTML/XML
    """
    for i in regexes:
        string = re.subn(i, '', string)[0]
    return string

if __name__ == '__main__':
    
    import os, sys
    import urllib2

    for i in sys.argv[1:]:
        if not i.startswith('http'):
            i = 'file://%s' % os.path.abspath(i)
        string = detag(urllib2.urlopen(i).read())
        string = '\n\n'.join([ i for i in string.split('\n\n') if i])
                               
        print string
