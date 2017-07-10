#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import time
sys.path.append('/Users/askar/Desktop/work/work/TheSun/ML/Controller')
from LocationController import *
from StringController import *

query_address = ""

def address_equals(given_str, to_find):
    given_str = StringController.delete_leading_symbols(given_str, ' .,')
    given_str = StringController.delete_trailing_symbols(given_str, ' .,')
    to_find = StringController.delete_leading_symbols(to_find, ' .,')
    to_find = StringController.delete_trailing_symbols(to_find, ' .,')

    given_str = unicode(given_str, encoding = 'utf-8').lower()
    to_find = unicode(to_find, encoding = 'utf-8').lower()

    if given_str == to_find:
    	return True
    return False

def isNumeric(given_str):
	for ch in given_str:
		if (ord(ch) < ord('0') or ord(ch) > ord('9')) and ch != '\\' and ch != '/':
			return False
	return True

def house_number(given_str):
	result = []
	arr = given_str.split(' ')

	last_numbers = 0
	if len(arr) > 0 and isNumeric(arr[-1]):
		last_numbers = 1
	if len(arr) > 1 and isNumeric(arr[-2]) and not isNumeric(arr[-1]):
		last_numbers = 2

	if last_numbers == 2:
		result += [arr[-2]]
		result += [arr[-2] + arr[-1]]
	if last_numbers == 1:
		result += [arr[-1]]
	return result

def house_street(given_str):
	result = []
	arr = given_str.split(' ')

	last_numbers = 0
	if len(arr) > 0 and isNumeric(arr[-1]):
		last_numbers = 1
	if len(arr) > 1 and isNumeric(arr[-2]) and not isNumeric(arr[-1]):
		last_numbers = 2

	if len(arr) > last_numbers:
		result += [arr[0]]
	if len(arr) > last_numbers + 1:
		result += [arr[0]]
		for i in range(1, len(arr) - last_numbers):
			result[1] += " " + arr[i]
	return result

def check(house_address, geo_object_list):
	if len(geo_object_list) == 1:
		return (True, LocationController.get_geocode_from_geo_object(geo_object_list[0]))

	house_address = [
						StringController.delete_trailing_symbols
						(
							StringController.delete_leading_symbols(item, ' .,'),
							' .,'
						)
						for item in house_address
					]

	check_list = []
	house_street_var = house_street(house_address[-1]) 

	if len(house_street_var) > 0:
		check_list += [house_street_var[0]]

	house_number_var = house_number(house_address[-1])
	if len(house_number_var) > 0:
		check_list += [house_number_var[0]]

	check_list += [house_street_var[i] for i in range(1, len(house_street_var))]
	check_list += [house_address[i] for i in range(0, len(house_address) - 1)]
	check_list += [house_number_var[i] for i in range(1, len(house_number_var))]

	for item in check_list:
		geo_object_list = LocationController.filter_geo_object_list(geo_object_list,
																	filter_str = unicode(item, encoding = 'utf-8'))
		if len(geo_object_list) == 1:
			return (True, LocationController.get_geocode_from_geo_object(geo_object_list[0]))

	return (False,)

def add_prefix(house_address):
	if 	address_equals(house_address[-1].split(' ')[0], 'Абая') or\
		address_equals(house_address[-1].split(' ')[0], 'Абай') or\
		address_equals(house_address[-1].split(' ')[0], 'Достык') or\
		(address_equals(house_address[-1].split(' ')[0], 'Аль') and\
			address_equals(house_address[-1].split(' ')[1], 'Фараби')) or\
		address_equals(house_address[-1].split(' ')[0], 'Аль-Фараби'):
		house_address[-1] = "проспект" + house_address[-1]
		return house_address
	return []

def get_geo_code(address):
	address = StringController.before(address, '—')

	house_address = []
	while StringController.after(address, ', ') != '':
		house_address += [StringController.before(address, ', ')]
		address = StringController.after(address, ', ')
	house_address += [address]

	address = 'Казахстан, Алматы, ' + house_address[-1]
	global query_address
	query_address = address

	address = StringController.to_utf8(address)

	for i in range(0, 10):
		json_object = LocationController.query_address(address)
		geo_object_list = LocationController.get_geo_object_list(json_object)
		if len(geo_object_list) > 0:
			break
		print "Trying to get data..."
		time.sleep(2)

	
	geo_object_list = LocationController.filter_geo_object_list(geo_object_list,
																kind = unicode('house', encoding = 'utf-8'))
	geo_object_list = LocationController.filter_geo_object_list(geo_object_list,
																filter_str = unicode('Казахстан', encoding = 'utf-8'))
	geo_object_list = LocationController.filter_geo_object_list(geo_object_list,
																filter_str = unicode('Алматы', encoding = 'utf-8'))
	
	if check(house_address, geo_object_list)[0] == True:
		return check(house_address, geo_object_list)[1]
	
	house_address = add_prefix(house_address)
	if len(house_address) == 0:
		return unicode("0 0", encoding = 'utf-8')

	if check(house_address, geo_object_list)[0] == True:
		return check(house_address, geo_object_list)[1]
	return unicode("0 0", encoding = 'utf-8')


db = MySQLdb.connect(host   = 'localhost',
                     user   = 'askar',
                     passwd = '',
                     db     = 'KRISHA_DATA')

cur = db.cursor()
cur.execute('select id, address, last_update_script from Houses');

cnt = 0
i = 0
res = cur.fetchall()
for row in res:
	i += 1
	if i < 23000:
		continue
	updated_script = row[2]
	if updated_script == '2':
		continue

	geo_code = get_geo_code(row[1])
	if geo_code != unicode("0 0", encoding = 'utf-8'):
		cnt += 1
		sql = "UPDATE Houses SET last_update_time=" + str(int(time.time()))
		sql += ", last_update_script=" + str(2)
		sql += ", geocode_long=" + geo_code.split(' ')[0]
		sql += ", geocode_lat=" + geo_code.split(' ')[1]
		sql += " where id=" + str(row[0])
		cur.execute(sql);
		db.commit()
		print unicode(query_address, encoding = 'utf-8')

print (cnt + 0.0) / i * 100
db.close()
