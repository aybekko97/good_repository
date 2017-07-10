#!usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import telebot
import cherrypy
import config
import requests
from telebot import types
from flat import Flat
from validations import *

import pandas as pd

import sys
sys.path.append("thesun/ML/Controller/")
sys.path.append("thesun/ML/")
from System import *

system = System()

system.choose_model()
system.train_model()

from AddressHandler import *

import myapiai

WEBHOOK_HOST = '146.185.158.146'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)

flat_dict = {}
step = {}

# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

def in_step_handler(chat_id):
	if (step.get(chat_id,0) == 0 or step.get(chat_id,0) == None):
		return False
	return True

# Хэндлер на команды /start и /help
@bot.message_handler(commands=['help', 'start'])
def welcome_message(message):
	wlc_msg = "Привет!\nТы обратился к боту, который сможет предсказать цену для твоей недвижимости. 🏡 ➡ 💰"
	help_msg = "*/ask* - чтобы предоставить данные вашей недвижимости для определения цены"
	bot.send_message(message.chat.id, wlc_msg+"\n\n"+help_msg, parse_mode="Markdown")


roomSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=5)
roomSelect.add(*room_list)

houseTypeSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
houseTypeSelect.add(*house_type_list)

hostelSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
hostelSelect.add(*yes_no_list)

regionSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
regionSelect.add(*region_list)

stateSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
stateSelect.add(*state_list)

phoneSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
phoneSelect.add(*phone_list)

internetSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
internetSelect.add(*internet_list)

bathroomSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
bathroomSelect.add(*bathroom_list)

balconySelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
balconySelect.add(*balcony_list)

balconyIsGlazedSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
balconyIsGlazedSelect.add(*yes_no_list)

doorSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
doorSelect.add(*door_list)

parkingSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
parkingSelect.add(*parking_list)

furnitureSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
furnitureSelect.add(*furniture_list)

flooringSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
flooringSelect.add(*flooring_list)




attributes = ['room_number',  #0
              'house_type', #1
              'built_time', #2
              'floor', #3
              'all_space', #4
              'living_space', #5
              'kitchen_space', #6
              'at_the_hostel', #7
              'region', #8
              'map_complex', #9
              'addr_street', #10
	      'addr_number', #11
              'state', #12
              'phone', #13
              'internet', #14
              'bathroom', #15
              'balcony', #16
              'balcony_is_glazed', #17
              'door', #18
              'parking', #19
              'furniture', #20
              'flooring', #21
              'ceiling'] #22

to_ask = [True, True, True, False,
	  True, False, False, False,
	  False, False, True, True,
	  False, False, False, False,
          False, False, False, False,
          False, False, False]
'''
to_ask = [True] * 23
'''
questions = ['Сколько комнат в квартире?',
             'Какой тип строения у квартиры?',
             'Год постройки дома(сдачи в эксплуатацию)?',
             'На каком этаже находится квартира? (прим. "7 из 10")',
             'Какова общая площадь? (прим. "75.5" м2)',
             'Какова площадь жилой комнаты? (прим. "41" м2)',
             'Какова площадь куханной? (прим. "12.2" м2)',
             'Квартира входит в привелегии общежитии?',
             'В каком районе находится?',
             'Жилой комплекс в котором находится дом? (прим. "нет" или "Нурлы Тау")',
             'Улица или микрорайон?',
	     "Номер дома?",
             'В каком состоянии находится дом?',
             'Тип телефона в вашем доме?',
             'Какой вид интернета имеется в вашем доме?',
             'Тип санузела(ванная,туалет)?',
             'Какого типа балкон?',
             'Балкон остеклен?',
             'Тип входной двери?',
             'Какая парковка есть рядом?',
             'Насколько мебелирована квартира?',
             'Каким материалом покрыт пол?',
             'Высота потолков в квартире? (прим. "2.9" в метрах)']


selections = [roomSelect,
              houseTypeSelect,
              None,
              None,
              None,
              None,
              None,
              hostelSelect,
              regionSelect,
              None,
              None,
	      None,
              stateSelect,
              phoneSelect,
              internetSelect,
              bathroomSelect,
              balconySelect,
              balconyIsGlazedSelect,
              doorSelect,
              parkingSelect,
              furnitureSelect,
              flooringSelect,
              None]

validations = [ validate_room,
         	validate_house_type,
		validate_built_time,
		None,
		validate_all_space,
		None,
		None,
		None,
		None,
		None,
		validate_addr_street,
		None,
		None,
		None,
		None,
		None,
		None,
		None,
		None,
		None,
		None,
		None,
		None]

dflt = {'room_number' : 3,  #0
              'house_type' : 'панельный', #1
              'built_time' : '1980', #2
              'floor' : '0', #3
              'all_space' : '0', #4
              'living_space' : '0', #5
              'kitchen_space' : '0', #6
              'at_the_hostel' : 'нет', #7
              'region' : '', #8
              'map_complex' : '', #9
              'addr_street': '', #10
	      'addr_number': '', #11
              'state' : '', #12
              'phone' : '', #13
              'internet': '', #14
              'bathroom' : '', #15
              'balcony' : '', #16
              'balcony_is_glazed' : '', #17
              'door' : '', #18
              'parking' : '', #19
              'furniture' : '', #20
              'flooring' : '', #21
              'ceiling': '3.0'}
@bot.message_handler(commands=['ask'])
def ask(message):
    try:
        chat_id = message.chat.id
        prev_step = step.get(chat_id, None)
        cur_step = prev_step
        if (cur_step is None):
        	cur_step = 0
        else:
        	prev_step -= 1
        if (chat_id not in flat_dict):
        	flat_dict[chat_id] = Flat()
        while(cur_step < len(questions) and to_ask[cur_step] == False):
        	cur_step += 1
        #print(cur_step, prev_step)
        print("ok")
        if (prev_step is not None):
        	print(message.text)
        	flat = flat_dict[chat_id]
        	if (validations[prev_step] is not None):
        		vl = validations[prev_step](message.text)
       			if (isinstance(vl,bool)):
        			msg = bot.send_message(chat_id, "неправильно, введите еще раз, пожалуйста.")
        			bot.register_next_step_handler(msg, ask)
        			return
        		setattr(flat,attributes[prev_step], vl)
        	else:
        		setattr(flat,attributes[prev_step], message.text)
        if (cur_step < len(questions)):
            msg = bot.send_message(chat_id, '*'+questions[cur_step]+'*', reply_markup=selections[cur_step], parse_mode="Markdown")
            bot.register_next_step_handler(msg, ask)
            step[chat_id] = cur_step + 1
        else:
            data = flat.__dict__
            if (type(data['addr_number']) == int):
            	data['addr_number'] = unicode(data['addr_number'])
            print(type(data['addr_street']), type(data['addr_number']))
            data['address'] = data['addr_street'].encode('utf-8') + ' ' + data['addr_number'].encode('utf-8')
            geocode = get_geo_code(data['address'])
            data['geocode_lat'] = geocode.split(' ')[1]
            data['geocode_long'] = geocode.split(' ')[0]
            for attr in attributes:
            	if (attr not in data):
            		data[attr] = dflt[attr]
            del data['addr_street']
            del data['addr_number']
            if ('type' in data): del data['type']
	    if ('dtype' in data): del data['dtype']
            print(data)
            data['id'] = 0
            data['price'] = '0'
            data['last_update_script'] = ''
            data['last_update_time'] = ''
            data['room_number'] = int(data['room_number'])
            df = pd.DataFrame(data, index=[0])
            print(df.head())
            print(df.dtypes)
            msg = bot.send_message(chat_id, "Calculating...")
            bot.send_message(chat_id, "Я думаю, подходящая цена - " + str(system.model.predict_price(df)['price'][df.index[0]] ) )
            step[chat_id] = None
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так.\n Лог ошибки: %s' % (e.strerror) )
        step[message.chat.id] = 0



@bot.message_handler(func=lambda message: in_step_handler(message.chat.id) == False, content_types=['text'])
def echo_message(message):
	bot.reply_to(message, myapiai.get_response(message.text))


# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
