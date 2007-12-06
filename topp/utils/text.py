import re

whitespace_pattern = re.compile('\s+')
def strip_extra_whitespace(title):
    if title is None:
        return ''
    title = whitespace_pattern.sub(' ', title).strip()
    return title.strip()
