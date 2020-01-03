import requests

class mudfish_client():
    def __init__(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Referer': 'http://ping.mudfish.net/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.s = requests.session()
        self.s.headers.update(self.headers)
        self.URL = 'http://127.0.0.1:8282'

    # 取得mudfish client版本等資料
    def get_mudfish_status(self):
        url = self.URL + '/do/mudrun/status'

        response = self.s.get(url)
        return response.json()

    # 授權client
    def auth(self, user_name, password, token, jwt):
        url = self.URL + '/do/auth'

        data = {
            "username": user_name,
            "password": password,
            "remember_me": False,
            "token": token,
            "jwt": jwt,
            "expert_mode": 0,
            "lang": "zh",
            "alias_enable": 0
        }

        response = self.s.post(url, json=data, verify=False)
        return response.json()

    def mudfish_start(self):
        url = self.URL + '/do/mudfish/start'
        response = self.s.post(url)
        return response.json()

    def mudfish_stop(self):
        url = self.URL + '/do/mudfish/stop'
        response = self.s.post(url)
        return response.json()

    # 取得進度
    def get_config_progress(self):
        url = self.URL + '/do/getconfprogress'
        response = self.s.get(url)
        return response.json()