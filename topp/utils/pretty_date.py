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

try:
    from DateTime import DateTime as zopedt
except ImportError:
    class zopedt: pass

def _date_diff(date1, date2):
    if isinstance(date1, zopedt):
        return date1.JulianDay() - date2.JulianDay()
    else:
        return date1.toordinal() - date2.toordinal()

def _date_compare(date1, date2):
    if isinstance(date1, zopedt):
        return date1.year() == date2.year()
    else:
        return date1.year == date2.year

def _pretty_date_engine(now, date):
    diff = _date_diff(date, now)
    if diff == -1:
	    return 'Yesterday'
    if diff == 0:
	    return 'Today'
    if diff == 1:
	    return 'Tomorrow'
    if 0 < diff < 7:
	    return date.strftime('%A')
    if diff < 90 and _date_compare(date, now):
	    return date.strftime('%B%e')
    return date.strftime('%B%e, %Y')
        
def prettyDate(date):
    if isinstance(date, zopedt):
        now = zopedt()
    else:
        now = date.today()
    return _pretty_date_engine(now, date)

if __name__ == '__main__':
    def test_pretty_date():
        from datetime import date
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
            pd = _pretty_date_engine(now, dates[d])
            try:
                assert pd == d
            except AssertionError:
                print "** Test failed: expected %s, got %s" % (d, pd)
                
    test_pretty_date()
    print "Tests completed."
