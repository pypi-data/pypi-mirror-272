import logging
import os
import socket

import requests
from logging import Logger
logger = Logger(__name__)


class RpaBrowserClient:
    def __init__(self):
        # self.browser_server_host = os.environ.get('BROWSER_SERVER_HOST', '127.0.0.1')
        self.browser_server_domain_host = os.environ.get('BROWSER_SERVER_HOST')
        domain, port = self.browser_server_domain_host.split(':')
        ip_host = socket.gethostbyname(domain)
        self.browser_server_ip_host = f'{ip_host}'
        self.browser_server_url = f'http://{self.browser_server_ip_host}:{port}'

    def get_cdp_info(self, user_id=None, platform_id=None, bw_args=None):
        if bw_args is None:
            bw_args = []
        rq_url = self.browser_server_url + '/get_browser'
        bw_args.append('--window-size=1920,1080')

        # if self.headless:
        #     bw_args.append('--headless')

        rq_json = {
            'user_id': user_id or 'Default',
            'platform_id': platform_id or 'Default',
            'bw_args': bw_args,

        }

        rsp = requests.post(rq_url, json=rq_json)
        if not rsp.ok:
            logger.info(f"远程CDP出现错误, 请检查")
            raise
        bw_info = rsp.json()
        # data_id = bw_info['data_id']
        # url = bw_info['cdp_url']
        # post = bw_info['cdp_url']
        bw_info['cdp_url'] = bw_info['cdp_url'].replace('127.0.0.1', self.browser_server_ip_host)
        return bw_info

    def get_cdp_url(self, user_id=None, platform_id=None, bw_args=None):
        bw_info = self.get_cdp_info(user_id, platform_id, bw_args)
        return bw_info['cdp_url']


if __name__ == '__main__':
    rbc = RpaBrowserClient()
    print(rbc.get_cdp_url())
