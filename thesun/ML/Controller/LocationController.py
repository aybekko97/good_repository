#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json 
from StringController import *

class LocationController:

	#accepts unicode address
	@staticmethod
	def query_address(address):
		query = unicode("https://geocode-maps.yandex.ru/1.x/?format=json" + \
				"&geocode=", encoding = 'utf-8') + address
		#print urllib2.urlopen(query).read()
		response = json.loads(urllib2.urlopen(query).read())
		#print query

		return response

	@staticmethod
	def get_geo_object_list(json_object):
		result = StringController.find_value_of_key(json_object, unicode('featureMember', encoding = 'utf-8'))
		if result[0] == False:
			return []
		return result[1]

	@staticmethod
	def get_geocode_from_geo_object(geo_object):
		result = StringController.find_value_of_key(geo_object, unicode('pos', encoding = 'utf-8'))
		if result[0] == False:
			return ""
		return result[1]

	@staticmethod
	def check_geo_object(geo_object, kind = '', filter_str = ''):

		filter_str = StringController.delete_symbols(filter_str, '., ')
		filter_str = filter_str.lower()
		
		new_filter_str = ""
		in_scope = 0
		for ch in filter_str:
			if ch == '(':
				in_scope += 1
			elif ch == ')':
				in_scope -= 1
			elif in_scope == 0:
				new_filter_str += ch

		filter_str = new_filter_str

		components = []
		result = StringController.find_value_of_key(geo_object, unicode('Components', encoding = 'utf-8'))
		if result[0] == True:
			components = result[1]

		result = StringController.find_value_of_key(geo_object, unicode('kind', encoding = 'utf-8'))
		if result[0] == False and kind != '':
			return False
		if kind != '' and result[1] != kind:
			return False

		names = []
		for component in components:
			names += [unicode(component['name']).lower()]

		for name in names:
			if StringController.lcs(name, filter_str):
				return True
		
		return False
		
	@staticmethod
	def filter_geo_object_list(geo_object_list, kind = '', filter_str = ''):

		new_geo_object_list = []
		for geo_object in geo_object_list:
			if LocationController.check_geo_object(geo_object, kind, filter_str):
				new_geo_object_list += [geo_object]

		return new_geo_object_list


