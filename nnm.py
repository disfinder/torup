#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2015-03-09

@author: okovalev
'''
from constants import NNM
import params
from string import strip
import urllib, urllib2, cookielib


def save_torrent(binary_data, fname):
    f = open(NNM.out_dir + fname + '.torrent', 'wb')
    f.write(binary_data)
    f.close()

# argparcer=params.create_common_parser()
# params=argparcer.parse_args()

params.username='disfinder'
params.password='f,shdfku'

# try to login
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

post_params = urllib.urlencode({
    'username' : params.username,
    'password' : params.password,
    'autologin':'on',
    'login'    : NNM.login
})
 
print 'Init and auth...'
# авторизация + сессия с куками
web_obj = opener.open('http://nnm-club.me/forum/login.php', post_params)
data = web_obj.read()
print 'Done.'



try:
    ids_file = open(NNM.id_filename, 'r')
    ids = ids_file.readlines()
    ids_file.close()
    
    data_file = open(NNM.data_filename, 'r')
    data = data_file.readlines()
    data_file.close()
except IOError:
    print 'err opening file'
    ids = []
    
    
# открытие на запись для новых "размеров" в last.lst
data_file = open(NNM.data_filename, 'w')
    
data_dict = {}  # data dict 
for current in data:
    current = strip(current)
    data_dict[str.split(current)[0]] = str.split(current)[1]
    

print 'Processing torrents ids:'
print '-----------------------'    
for torrent_id in ids:
    torrent_id = strip(torrent_id)
    full_file_string = torrent_id
    # if torrent_id.count(NNM.comment_symbol) > 0:
    #     torrent_id = strip(torrent_id[:torrent_id.find(NNM.comment_symbol)])
    if NNM.comment_symbol in torrent_id:
        torrent_id=torrent_id[:torrent_id.find(NNM.comment_symbol)]

    if (len(torrent_id)==0):
        continue
    download_url = NNM.tracker_prefix + torrent_id
    web_obj = opener.open(download_url, post_params)
    data = web_obj.read()
    
    try:
        if len(data) <> int (data_dict[torrent_id]):
            # updated torrent
            print '[^]', full_file_string
            save_torrent(data, torrent_id)
        else:
            # not updated, same size
            print '[=]', full_file_string
    except (IndexError, KeyError):
        # new torrent
        print '[+]', full_file_string
        save_torrent(data, torrent_id)
    data_file.write(str(torrent_id) + ' ' + str(len(data)) + '\n')
                
 
data_file.close()  
    
