#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# created by x0x01 (aka.x0x01[AT]gmail[dot]com)
 
import urllib, urllib2, cookielib
from string import strip
 
LOGIN   = 'disfinder'
PASS    = '16777216-1'
# путь для сохранения torrent файла
OUT_DIR = './'
#OUT_DIR = '/tmp/gettor/'
 
# формирование кук
post_params = urllib.urlencode({
    'login_username' : LOGIN,
    'login_password' : PASS,
    'login' : '%C2%F5%EE%E4'
})
 
# инит обработчика кук
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
 
# авторизация + сессия с куками
web_obj = opener.open('http://login.rutracker.org/forum/login.php', post_params)
data = web_obj.read()
 
try:
    # читаем файл со ссылками, формируем список
    fl_url_list = open('urls.lst', 'r')
    url_arr = fl_url_list.readlines()
    fl_url_list.close()
    # чтение файла "размеров", формируем список
    fl_dta_list = open('last.lst', 'r')
    dta_arr = fl_dta_list.readlines()
    fl_dta_list.close()
except IOError:
    print 'err'
    dta_arr = []
 
 
# открытие на запись для новых "размеров" в last.lst
fl_dta_list = open('last.lst', 'w')
 
# из списка "размеров" формируем словарь ID:SIZE
dta_dic = {}
for curr in dta_arr:
    # отрезаем переносы строк
    curr = strip(curr)
    # делим строку по пробелу и создаем словарь
    dta_dic[str.split(curr)[0]] =  str.split(curr)[1]
 
# сохранение torrent файла
def dw_torrent_f(b_data, f_name):
    f = open(OUT_DIR+f_name+'.torrent', 'w')
    f.write(b_data)
    f.close()
 
# обработка ссылок
for thread_url in url_arr:
    # отрезаем переносы строк
    thread_url = strip(thread_url)
    # делим ссылку на 2 части (получение id форума)
    topic_id = str.split(thread_url,'=')[1]
    dl_torrent_url = 'http://dl.rutracker.org/forum/dl.php?t='+topic_id
    # получение torrent файла по ссылке
    web_obj = opener.open(dl_torrent_url, post_params)
    data = web_obj.read()
    # сравнение размеров полученного файла и в last.lst
    try:
        if len(data) <> int(dta_dic[topic_id]):
            # этот обновился, сохраняем
            print '[^]', thread_url
            dw_torrent_f(data, topic_id)
    except (IndexError, KeyError):
        # этот новый, сохраняем
        print '[+]', thread_url
        dw_torrent_f(data, topic_id)
        #print 'UPD:', dl_torrent_url, 'new:', len(data), 'old:', m_dic[topic_id]
    # пишем в last.lst новые значения id и размер
    fl_dta_list.write(str(topic_id)+' '+str(len(data))+'\n')
 
# закрытие файла
fl_dta_list.close()