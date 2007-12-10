import doctest
import re
import string
import unittest

whitespace_pattern = re.compile('\s+')
def strip_extra_whitespace(title):
    if title is None:
        return ''
    title = whitespace_pattern.sub(' ', title).strip()
    return title.strip()

def valid_title(title):
    """
    Alphanumeric is ok with punctuation and whitespace::
    
    >>> valid_title('title 1!')
    True

    Unicode is ok (though you will get an ugly id)::

    >>> valid_title('\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e')
    True

    Punctuation is a no go::

    >>> valid_title('"!"& ^"")""')
    False

    As is whitespace::

    >>> valid_title('\t ')
    False

    """
    if len(title) < 2: return False
    for c in title:
        if not _ignore.get(c):
            if c.isalnum(): # catch alphanumerics
                return True
            if not _printable.get(c): # catch unicode chars but not
                                     # whitespace or escapes
                return True
    return False

def valid_id(id):
    # projects ids are more strict than titles
    if not valid_title(id): return False

    valid_chars = string.letters + string.digits + '-_'
    for c in id:
        if c not in valid_chars:
            return False
    return True

_ignore = dict((char, True) for char in ''.join((string.punctuation, string.whitespace)))
_printable = dict((char, True) for char in string.printable)

def test_suite():
    unit = doctest.DocTestSuite('topp.utils.text',
                                optionflags=doctest.ELLIPSIS)
    return unit

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
