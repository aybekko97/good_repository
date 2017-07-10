#!/usr/bin/python
# -*- coding: utf-8 -*-

room_list = ['1','2','3','4','5','6','7','8','9']

house_type_list = ['кирпичный','панельный','монолитный','каркасно-камышитовый','иное']

region_list =  ['Алатауский р-н',
                 'Алмалинский р-н',
                 'Ауэзовский р-н',
                 'Бостандыкский р-н',
                 'Жетысуский р-н',
                 'Медеуский р-н',
                 'Наурызбайский р-н',
                 'Турксибский р-н']

state_list = ['хорошее',
                 'среднее',
                 'евроремонт',
                 'требует ремонта',
                 'свободная планировка',
                 'черновая отделка']

phone_list = ['отдельный',
               'блокиратор',
               'есть возможность подключения',
               'нет']

internet_list = ['ADSL',
                 'через TV кабель',
                 'проводной',
                 'оптика',
                 'нет']

bathroom_list = ['раздельный',
                   'совмещенный',
                   '2 с/у и более',
                   'нет']

balcony_list = ['балкон',
                  'лоджия',
                  'балкон и лоджия',
                  'несколько балконов и лоджий',
                  'нет']

yes_no_list = ['да',
               'нет']

door_list = ['деревянная',
               'металлическая',
               'бронированная']

parking_list = ['паркинг',
                  'гараж',
                  'рядом охр. стоянка',
                  'нет']

furniture_list = ['полностью меблирована',
                    'частично меблирована',
                    'пустая']

flooring_list = ['линолеум',
                   'паркинг',
                   'ламинат',
                   'дерево',
                   'ковролан',
                   'плитка',
                   'пробковое']

def validate_room(msg):
	room_cnt = ''.join([c for c in msg if c in '1234567890.']).strip()
	if (room_cnt.isdigit() and int(room_cnt) > 0 and int(room_cnt) < 10):
		return room_cnt
	else:
		return False

def validate_house_type(msg):
	if (msg.strip().lower() in map(lambda s: unicode(s,'utf-8'), house_type_list)):
		return msg.strip().lower()
	return False

def validate_built_time(msg):
	built_time = ''.join([c for c in msg if c in '1234567890. ']).strip()
	if (built_time.isdigit() and int(built_time) > 1900 and int(built_time) < 2017):
		return built_time
	else:
		return False

def validate_all_space(msg):
	all_space = ''.join([c for c in msg if c in '1234567890. ']).strip()
	try:
		if (float(all_space) > 20 and float(all_space) < 300):
			return all_space
		else:
			return False
	except:
		return False

def validate_addr_street(msg):
	return msg

def validate_addr_number(msg):
	return msg
