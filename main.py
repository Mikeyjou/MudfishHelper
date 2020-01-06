#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import time
import warnings
import configparser

import requests

from bs4 import BeautifulSoup
from getpass import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

from api import mudfish_api
from client import mudfish_client

class mudfish_helper():
    def __init__(self):
        self.api = mudfish_api()
        self.client = mudfish_client()
        self.AUTH_KEY = None
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def login(self):
        try:
            status = self.client.get_mudfish_status()
        except:
            print('請先開啟mudfish控制面板')
            exit()
        if status:
            user_name = self.config['account']['username']
            password = self.config['account']['password']
            if not user_name or not password:
                user_name = input('帳號: ')
                password = getpass('密碼: ')

            login_response = self.api.sign_in(user_name, password, status['version'])
            
            if login_response['status'] == 200:
                auth_response = self.client.auth(user_name,password, login_response['token'], login_response['jwt'])
                self.AUTH_KEY = login_response['jwt']
                if auth_response['status'] == 200:
                    print('登入成功!!')
                else:
                    print('授權失敗!!')
                    exit()
            else:
                print('登入失敗!!')
                exit()
        else:
            print('無法從控制面板取得資料')

    def user_item_choose(self):
        user_data = self.api.get_user_status(self.AUTH_KEY)
        user_items = user_data['data']['user']['items']
        if len(user_items) > 0:
            print('')
            print('使用者有以下物品: ')
            for index, item in enumerate(user_items):
                print('({0}) {1}'.format(index+1, item['name']).encode('cp950', errors='ignore').decode('utf-8'))
            
            while True:
                item_choice = int(input('選擇物品: '))
                if item_choice > 0 and item_choice <= len(user_items):
                    break
        else:
            print('')
            print('使用者沒有物品可以修改，請先手動創建物品！')

        return user_items[int(item_choice)-1]

    def vpn_connect(self, user_item, game_ip):
        print('')
        print('開始找尋合適節點..')
        ping_result = self.api.get_ping_result(game_ip)

        if len(ping_result) > 0:
            print('有以下合適節點:')
            for index, ping in enumerate(ping_result):
                print('({0}) {1} Avg:{2}'.format(index+1, ping['location'], ping['ping_result']['rtt_avg']))

            while True:
                node_choice = int(input('選擇節點: '))
                if node_choice > 0 and node_choice <= len(ping_result):
                    break
            print('開始保存設定..')
            self.client.mudfish_stop()
            game_ips = game_ip.split('.')
            del game_ips[-1]
            self.api.modify_item(user_item['iid'], '.'.join(str(x) for x in game_ips) + '.0/24', self.AUTH_KEY)
            self.api.modify_conf(user_item['iid'], ping_result[int(node_choice)-1], self.AUTH_KEY)
            
            print('保存成功')

            self.client.logout()
            self.api.s.close()
            self.client.s.close()
            exit()
            # while True:
            #     response = self.client.get_config_progress()
            #     print('連線進度 {0}%'.format(float(response['total'])/float(response['count'])*100))
            #     if response['count'] == response['total']:
            #         print('成功連線!!')
            #         break
            #     time.sleep(0.5)

        else:
            print('沒有適合節點')
            exit()

    def vpn_disconnect(self):
        self.client.mudfish_stop()

    def main(self):
        self.login()
        user_item = self.user_item_choose()
        game_ip = input('遊戲IP: ')
        self.vpn_connect(user_item, game_ip)

        # while True:
        #     print('')
        #     print('(1)新連線')
        #     print('(2)更換節點')
        #     print('(3)關閉連線')
        #     print('(4)結束程式')
        #     mode = int(input('選擇操作: '))
        #     if mode == 1:
        #         self.login()
        #         user_item = self.user_item_choose()
        #         game_ip = input('遊戲IP: ')
        #         self.vpn_connect(user_item, game_ip)
        #     elif mode == 2:
        #         self.login()
        #         self.vpn_connect(user_item, game_ip)
        #     elif mode == 3:
        #         self.vpn_disconnect()
        #     elif mode == 4:
        #         exit()

if __name__ == '__main__':
    m = mudfish_helper()
    m.main()