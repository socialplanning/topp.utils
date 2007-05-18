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

from datetime import date as pydate
from datetime import datetime as pydatetime
try:
    from DateTime import DateTime as zopedatetime
except ImportError:
    class zopedatetime:
        _import_error = True


class DateWrapper(object):
    def __init__(self, date):
        self.date = date
        if isinstance(date, zopedatetime):
            self.now = zopedatetime()
            self.datediff = lambda d1, d2: d1.JulianDay() - d2.JulianDay()
            self.yeardiff = lambda d1, d2: d1.year() - d2.year()
        elif isinstance(date, pydate) or isinstance(date, pydatetime):
            self.now = pydate.today()
            self.datediff = lambda d1, d2: d1.toordinal() - d2.toordinal()
            self.yeardiff = lambda d1, d2: d1.year - d2.year
        else:
            raise ValueError('pretty_date: Unknown date object: %s' % date.__class__) # TODO

    def prettystr(self):
        diff = self.datediff(self.date, self.now)
        if diff == -1:
            return 'Yesterday'
        if diff == 0:
            return 'Today'
        if diff == 1:
            return 'Tomorrow'
        if 0 < diff < 7:
            return self.date.strftime('%A')
        if diff < 90 and self.yeardiff(self.date, self.now) == 0:
            return self.date.strftime('%B %-e')
        return self.date.strftime('%B %-e, %Y')


        
def prettyDate(date):
    date = DateWrapper(date)
    return date.prettystr()



if __name__ == '__main__':
    def test(date=pydate):
        """relies on being able to construct the passed-in type of date
        with YYYY, mm, dd"""
        now = date(2006, 1, 1)
        dates = {
            'Today' : date(2006, 1, 1),
            'Tomorrow' : date(2006, 1, 2),
            'Yesterday' : date(2005, 12, 31),
            'Tuesday' : date(2006, 1, 3),
            'Saturday' : date(2006, 1, 7),
            'January 8' : date(2006, 1, 8),
            'December 8, 2006' : date(2006, 12, 8),
            'January 8, 2007' : date(2007, 1, 8)
            }
        
        for d in dates:
            wrapped = DateWrapper(dates[d])
            wrapped.now = now
            expected = wrapped.prettystr()
            try:
                assert d == expected
            except AssertionError:
                print "** Test failed: expected %s, got %s" % (d, expected)
                

    test(date=pydate)
    test(date=pydatetime)
    if not zopedatetime._import_error:
        test(date=zopedatetime)

    try:
        prettyDate('not a date')
        assert 0
    except ValueError, e:
        assert "Unknown date object: <type 'str'>" in e.args[0]

    print "Tests completed."
