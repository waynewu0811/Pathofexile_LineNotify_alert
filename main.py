# -*- coding: UTF-8 -*-
import tailer, requests
from playsound import playsound
import sys
import os.path
from os import path

import config


str = sys.path[0]
file = eval(repr(str).replace('\\', '/'))
sound_file_path = file + '//Rhodesmas_Notif_1.wav'

def lineNotifyMessage(msg):
    #play alert sound
    playsound(sound_file_path)
    token = config.lineNotify_authtoken
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}

    #send post request to Line_notify
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    if r.status_code == 200:
        print("sending >> " + msg)
    return r.status_code



def main():
    #check log path if esixt
    if not os.path.isfile(config.game_log_path):
        print("ERROR : game_log_path not esixt!")
        return

    #tracking game log
    for line in tailer.follow(open(config.game_log_path, encoding = 'utf8'), delay=0.05):
        if 'ˇˇ' not in line:
            if "] @來自 " in line:      #2020/06/09 12:13:04 72356671 acf [INFO Client xxx] @來自 <公會> 遊戲ID: 內容
                message = '私人訊息\n' + line[line.find('] @來自 ')+6:]
                lineNotifyMessage(message)
                
            elif "] %" in line:         #2020/06/09 23:10:44 111816734 acf [INFO Client xxx] %<公會> 遊戲ID: 內容
                message = '隊伍訊息\n' + line[line.find('] %')+3:]
                lineNotifyMessage(message)

if __name__ == "__main__": 
    main() 