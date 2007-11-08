# WARNING: this file must be kept in sync with tasktracker/public/javascripts/pretty-date.js

# Copyright (C) 2006-2007 The Open Planning Project

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the 
# Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, 
# Boston, MA  02110-1301
# USA

from dateutil.parser import parse
from datetime import date as pydate
from datetime import datetime as pydatetime
try:
    from DateTime import DateTime as zopedatetime
except ImportError:
    class zopedatetime:
        _import_error = True


class DateWrapper(object):
    def __init__(self, date):
        if isinstance(date, basestring):
            # convert it to a pydatetime
            date = parse(date)
        if isinstance(date, pydatetime) or isinstance(date, pydate): # intentionally not elif
            self.now = pydate.today()
            self.datediff = lambda d1, d2: d1.toordinal() - d2.toordinal()
            self.yeardiff = lambda d1, d2: d1.year - d2.year
        elif isinstance(date, zopedatetime):
            self.now = zopedatetime()
            self.datediff = lambda d1, d2: d1.JulianDay() - d2.JulianDay()
            self.yeardiff = lambda d1, d2: d1.year() - d2.year()
        else:
            raise ValueError('pretty_date: Unknown date object: %s' % date.__class__)

        self.date = date

    def prettystr(self):
        """relies on self.date being a pydatetime or a zopedatetime
        (either way it will have a strftime method)"""
        diff = self.datediff(self.date, self.now)
        if diff == -1:
            return 'yesterday'
        if diff == 0:
            return 'today'
        if diff == 1:
            return 'tomorrow'
        if 0 < diff < 7:
            return self.date.strftime('%A')

        month = self.date.strftime('%B')
        day = self.date.strftime('%d')
        if day.startswith('0'):
            day = day[1:]
        month_day = ' '.join((month, day))

        if diff < 90 and self.yeardiff(self.date, self.now) == 0:
            return month_day

        year = self.date.strftime(', %Y')
        return month_day + year


        
def prettyDate(date):
    date = DateWrapper(date)
    return date.prettystr()



if __name__ == '__main__':

    def expectedmap(date_constructor=pydate):
        return {
            'today' : date_constructor(2006, 1, 1),
            'tomorrow' : date_constructor(2006, 1, 2),
            'yesterday' : date_constructor(2005, 12, 31),
            'Tuesday' : date_constructor(2006, 1, 3),
            'Saturday' : date_constructor(2006, 1, 7),
            'January 8' : date_constructor(2006, 1, 8),
            'December 8, 2006' : date_constructor(2006, 12, 8),
            'January 8, 2007' : date_constructor(2007, 1, 8)
            }

    def date_str_constructor(*args):
        return '%4d-%02d-%02d' % args # expects 3 integers YYYY, MM, DD

    def test(date_constructor=pydate):
        """relies on being able to construct the passed-in type of date
        with YYYY, mm, dd"""
        if date_constructor == zopedatetime:
            now = zopedatetime(2006, 1, 1)
        else:
            now = pydatetime(2006, 1, 1)
        
        for expected, input in expectedmap(date_constructor).items():
            wrapped = DateWrapper(input)
            wrapped.now = now
            got = wrapped.prettystr()
            try:
                assert got == expected
            except AssertionError:
                print "** Test failed: expected %s, got %s" % (expected, got)
                
    test(date_constructor=date_str_constructor)
    test(date_constructor=pydate)
    test(date_constructor=pydatetime)
    if not hasattr(zopedatetime, '_import_error'):
        test(date=zopedatetime)

    try:
        prettyDate(['not a date'])
        assert 'we expected to throw an exception' == 0
    except ValueError, e:
        assert "Unknown date object: <type 'list'>" in e.args[0]

    print "Tests completed."
