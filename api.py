import requests
from bs4 import BeautifulSoup

class mudfish_api():
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
        self.PING_URL = 'http://ping.mudfish.net'
        self.API_URL = 'https://api.mudfish.net'

    def ping_page(self):
        url = self.PING_URL
        response = self.s.get(url)
        return response.text

    def get_all_nodes(self, body):
        soup = BeautifulSoup(body, 'lxml')
        result = []

        for node in soup.find_all('input', {'name': 'nodes[]'}):
            result.append({'location': node.get('location'), 'id': node.get('value')})

        return result

    def get_region_node_ids(self, all_nodes, country):
        result = []
        for node in all_nodes:
            if node['location'][:2] == country:
                result.append(node['id'])
        return result

    def start(self, node_ids, game_ip):
        url = self.PING_URL + '/ping/start/{0}'.format(game_ip)
        
        data = {
            'nodes': ','.join(node_ids)
        }

        response = self.s.post(url, data=data)
        return response.text

    def get_region_node_ips(self, body):
        soup = BeautifulSoup(body, 'lxml')
        trs = soup.find_all('tr')
        result = []
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) > 2:
                location = tds[0].getText()
                ip = tds[1].getText()
                node_id = tds[2].find('span').get('id').replace('result_', '')
                result.append({'id': node_id, 'location': location, 'ip': ip})
        return result

    def ping(self, nodes, game_ip):
        result = []
        for node in nodes:
            url = self.PING_URL + '/ping/{0}/{1}/{2}'.format(node['id'], node['ip'], game_ip)
            response = self.s.get(url)
            node['ping_result'] = response.json()
            if float(node['ping_result']['rtt_avg']) > 0 and node['ping_result']['result'] == 'UP':
                result.append(node)
        return sorted(result, key=lambda k: float(k['ping_result']['rtt_avg']))

    def get_ping_result(self, game_ip):
        body = self.ping_page()
        nodes = self.get_all_nodes(body)
        node_ids = self.get_region_node_ids(nodes, 'TW')
        response = self.start(node_ids, game_ip)
        ips = self.get_region_node_ips(response)
        ping_result = self.ping(ips, game_ip)
        return ping_result

    # 修改裝備
    def modify_item(self, item_id, ip, authorization):
        url = self.API_URL + '/item/custom'

        data = {
            'iid': item_id,
            'category_id': -1,
            'name': '5e',
            'icon_path': None,
            'rt_list': ip,
            'rtt_location': '',
            'rtt_ip': ''
        }

        response = self.s.post(url, data=data, files=[], verify=False, headers={'Authorization': authorization})
        return response.json()

    # 修改節點
    def modify_conf(self, item_id, node, authorization):
        url = self.API_URL + '/item/conf'

        data = {
            "iid": item_id,
            "active": 1,
            "adnmode": 0,
            "autorefresh": 0,
            "destinationRid": -1,
            "sidFrom": node['id'],
            "adnSidFrom": -1,
            "adnSidTo": -1
        }

        response = self.s.post(url, json=data, verify=False, headers={'Authorization': authorization})
        return response.json()

    def sign_in(self, user_name, password, version):
        url = self.API_URL + '/signin'

        data = {
            'username': user_name,
            'password': password,
            'remember_me': False,
            'version': version
        }

        response = self.s.post(url, data=data, files=[], verify=False)
        return response.json()

    def get_user_status(self, authorization):
        url = self.API_URL + '/graphql'
        data = {
            "query": """
                {
                    conf {          
                        defaultPriceKrw          
                        pmTimeBegin          
                        pmTimeEnd          
                        pmTimeStr        
                    }        
                    user {          
                        aliasUid          
                        dataPlan          
                        dataPlanChanged          
                        items {            
                            active            
                            iid            
                            rid            
                            name            
                            price            
                            currency            
                            iconPath            
                            iconUri            
                            destinationKey            
                            destinationName            
                            locationDeadfrom            
                            locationDeadto            
                            remainDays            
                            route            
                            routeAutoselect
                        }          
                        uid          
                        payCredits          
                        payCurrency          
                        payLasttime          
                        payExchangeRatefrom          
                        payExchangeRateto          
                        progConf {            
                            mudfishFullvpnSid            
                            mudfishFullvpnSidLocation            
                            mudfishFullvpnVid            
                            mudfishFullvpnVidLocation            
                            mudfishFullvpnXp            
                            mudfishMtu            
                            mudfishProtomethod            
                            mudflowCompatv1            
                            mudflowRttmethod          
                        }        
                    }        
                    mudfishVpnVersion     
                }
            """
        }

        response = self.s.post(url, json=data, verify=False, headers={'Authorization': authorization})
        return response.json()