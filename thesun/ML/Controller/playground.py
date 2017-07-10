#!/usr/bin/env python
# -*- coding: utf-8 -*-
from AddressHandler import *

s = unicode("мкр. Коктем-2 ", encoding = 'utf-8')
s = s.encode('utf-8')
geo_code = get_geo_code(s + str(2))
print geo_code