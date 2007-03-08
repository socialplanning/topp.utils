# WARNING: this file must be kept in sync with tasktracker/public/javascripts/pretty-date.js

# Copyright (C) 2006 The Open Planning Project

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

from datetime import datetime as pydt
from DateTime import DateTime as zopedt

def _date_diff_zope(date1, date2):
    return date1.JulianDay() - date2.JulianDay()

def _date_diff_py(date1, date2):
    return date1.toordinal() - date2.toordinal()

def _pretty_date_engine_zope(now, date):
    diff = _date_diff_zope(date, now)
    if diff == -1:
	    return 'yesterday'
    if diff == 0:
	    return 'today'
    if diff == 1:
	    return 'tomorrow'
    if 0 < diff < 7:
	    return date.strftime('%A')
    if diff < 90 and date.year() == now.year():
	    return date.strftime('%B %e')
    return date.strftime('%B %e, %Y')

def _pretty_date_engine_py(now, date):
    diff = _date_diff_py(date, now)
    if diff == -1:
	    return 'yesterday'
    if diff == 0:
	    return 'today'
    if diff == 1:
	    return 'tomorrow'
    if 0 < diff < 7:
	    return date.strftime('%A')
    if diff < 90 and date.year == now.year:
	    return date.strftime('%B %e')
    return date.strftime('%B %e, %Y')

def prettyDate(date):
    if isinstance(date, zopedt):
        now = DateTime()
        return _pretty_date_engine_zope(now, date)
    elif isinstance(date, pydt):
        now = date.today()
        return _pretty_date_engine_py(now, date)
