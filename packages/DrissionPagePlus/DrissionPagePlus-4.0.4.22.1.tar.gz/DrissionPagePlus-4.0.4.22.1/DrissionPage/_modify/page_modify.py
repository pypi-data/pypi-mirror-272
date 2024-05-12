import json
from logging import Logger
logger = Logger(__name__)

from DrissionPage import ChromiumPage
from DrissionPage._common.rpa_browser_client import RpaBrowserClient

rbc = RpaBrowserClient()


class RemotePage(ChromiumPage):
    rbc = RpaBrowserClient()

    def __new__(cls, user_id=None, platform_id=None, bw_args=None, tab_id=None,
                addr_or_opts=None, timeout=None, addr_driver_opts=None):

        user_id = user_id or 'Default'
        platform_id = platform_id or 'Default'
        bw_args = bw_args or [
            "--lang=zh",
            "--window-size=1920,1080"
        ]
        bw_info = cls.rbc.get_cdp_info(user_id, platform_id, bw_args)
        cdp_url = bw_info['cdp_url']

        start_args = {}
        if addr_or_opts:
            start_args['addr_or_opts'] = addr_or_opts
        if tab_id:
            start_args['tab_id'] = tab_id
        if timeout:
            start_args['timeout'] = timeout

        start_args['addr_driver_opts'] = addr_driver_opts or cdp_url
        r = super().__new__(cls, **start_args)

        r.user_id = user_id
        r.platform_id = platform_id
        r.bw_info = bw_info
        r.cdp_url = cdp_url
        return r

    def __init__(self, user_id=None, platform_id=None, bw_args=None, tab_id=None,
                 addr_or_opts=None, timeout=None, addr_driver_opts=None) -> object:

        self.user_id = user_id or 'Default'
        self.platform_id = 'Default' or platform_id
        self.bw_args = bw_args or [
            "--lang=zh",
            "--window-size=1920,1080"
        ]
        self.bw_info = self.bw_info or self.rbc.get_cdp_info(self.user_id, self.platform_id, self.bw_args)
        self.cdp_url = self.cdp_url or self.bw_info['cdp_url']
        logger.info(f"CDP地址: {self.cdp_url}")
        start_args = {}
        if addr_or_opts:
            start_args['addr_or_opts'] = addr_or_opts
        if tab_id:
            start_args['tab_id'] = tab_id
        if timeout:
            start_args['timeout'] = timeout
        if addr_driver_opts:
            start_args['addr_driver_opts'] = addr_driver_opts or self.cdp_url

        super().__init__(**start_args)

    def request(self, method,
                url,
                headers,
                params,
                post_query_mode=False,
                with_credentials=False
                ):
        # method = "GET"
        # url = "https://www.baidu.com"
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        # }
        # params = {}
        # post_query_mode = False
        # with_credentials = False
        request_txt = """
                        var method = "%(method)s";
                        var url = "%(url)s";
                        var headers = %(headers)s;
                        var params = %(params)s;
                        var post_query_format = %(post_query_format)s;
                        var xhr = new XMLHttpRequest();

                        if (%(with_credentials)s){
                            xhr.withCredentials = true;
                        };
                        xhr.open(method, url, false);

                        Object.keys(headers).forEach(function(key) {
                          xhr.setRequestHeader(key, headers[key]);
                        });

                        if (post_query_format){
                            data = new URLSearchParams(params);
                        } else {
                            data = JSON.stringify(params);
                        };

                        if (method == "GET") {
                            xhr.send();
                        } else if (method == "POST"){
                            xhr.send(data);
                        };
                        return xhr.responseText
                  """ % (
            {
                "method": method,
                "url": url,
                "headers": json.dumps(headers),
                "params": json.dumps(params),
                "post_query_format": 1 if post_query_mode else 0,
                "with_credentials": 1 if with_credentials else 0
            }
        )
        result = self.run_js(request_txt)
        return result


if __name__ == '__main__':
    user_bw = ('ee312122233e', 'Default', ['--lang=zh', '--window-size=1920,1080'])
    page = RemotePage(*user_bw, tab_id=None)
    page.get('https://www.baidu.com')
    page1 = RemotePage(*user_bw, tab_id=None)
    page2 = RemotePage(*user_bw, tab_id=None)
    page3 = RemotePage(*user_bw, tab_id=None)
    # page.get(url)
    method = "GET"
    url = "https://www.baidu.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    params = {}
    post_query_mode = False
    with_credentials = False
    page.get(url)
    z = page.request(method, url, headers, params, post_query_mode, with_credentials)
    print(page.tab_id)
