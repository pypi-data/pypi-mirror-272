#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : common
# Author        : Sun YiFan-Movoid
# Time          : 2024/2/21 19:22
# Description   : 
"""
import json

import psutil
import requests
from RobotFrameworkBasic import RobotBasic, RfError, robot_log_keyword


class BasicCommon(RobotBasic):
    def __init__(self):
        super().__init__()
        net_if_addrs = psutil.net_if_addrs()
        network_info = []
        for interface_name, interface_info in net_if_addrs.items():
            for info in interface_info:
                if info.family == 2:  # 只处理IPv4地址
                    network_info.append({'address': info.address, 'netmask': info.netmask})
        self.headers = {
            'Uinetworkinfo': json.dumps(network_info)
        }
        self._request_param = {}

    @robot_log_keyword
    def api_url_check(self, url: str):
        if url.startswith('http'):
            return url
        else:
            protocol_text = f'{self._config_config["protocol"]}://' if 'protocol' in self._config_config else 'http://'
            ip_text = self._config_config["ip"] if "ip" in self._config_config else "127.0.0.1"
            port_text = f':{self._config_config["port"]}' if "port" in self._config_config else ""
            path_text = f"/{self._config_config['url_path_header'].strip('/')}" if "url_path_header" in self._config_config else ""
            return f'{protocol_text}{ip_text}{port_text}{path_text}/' + url.lstrip('/')

    @robot_log_keyword
    def requests_ori(self, method, url, status=200, **kwargs):
        kwargs.setdefault('headers', self.headers)
        real_url = self.api_url_check(url)
        self._request_param = {'method': method, 'url': real_url, **kwargs}
        self.print(f'try to request:{self._request_param}')
        response = requests.request(method, real_url, **kwargs)
        self.print(f'get response success')
        if response.status_code == status:
            self.print(response.text)
            return response
        else:
            raise RfError(f'response status is {response.status_code}, not {status}.response is {response.text}.requests is {self._request_param}')

    def post_ori(self, url, status=200, **kwargs):
        return self.requests_ori('POST', url, status, **kwargs)

    def get_ori(self, url, status=200, **kwargs):
        return self.requests_ori('GET', url, status, **kwargs)

    @robot_log_keyword
    def requests(self, method, url, code=0, status=200, **kwargs):
        response = self.requests_ori(method, url, status, **kwargs)
        res_json = response.json()
        if res_json['code'] == code:
            return res_json['data']
        else:
            raise RfError(f'response code is {res_json["code"]}, not {code}.response json is {res_json}.requests is {self._request_param}')

    def post(self, url, code=0, status=200, **kwargs):
        return self.requests('POST', url, code, status, **kwargs)

    def get(self, url, code=0, status=200, **kwargs):
        return self.requests('GET', url, code, status, **kwargs)
