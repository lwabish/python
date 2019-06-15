import random
import requests
import http
import time

from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from http.client import IncompleteRead
from lxml import etree

uas = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.96 Chrome/58.0.30"
    "29.96 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/'
    '537.36'
]

# 需要pip install pysocks才能使requests支持socks5代理
proxy = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080',
}


def get_fund_value(id: str)-> float:
    url = 'http://fund.eastmoney.com/{}.html'.format(id)
    html = etree.HTML(get_content(url).text)
    return float(html.xpath('//*[@id="gz_gsz"]/text()')[0])


def set_header():
    """
    随机IP+随机User Agent
    """
    random_ip = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
        random.randint(0, 255)) + '.' + str(random.randint(0, 255))
    headers = {
        'User-Agent': random.choice(uas),
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        'X-Forwarded-For': random_ip,
    }
    return headers


def build_session(gfw=False, cookies=None):
    s = requests.Session()
    s.headers = set_header()
    s.proxies = proxy if gfw else None
    s.cookies = requests.utils.cookiejar_from_dict(
        cookies) if cookies else requests.utils.cookiejar_from_dict({})
    return s


def get_content(url, gfw=False, cookies=None):
    """
    服务器错误时重试+随机header
    """
    try:
        s = requests.Session()

        retries = Retry(total=5, backoff_factor=10,
                        status_forcelist=[500, 502, 503, 504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        return s.get(url, headers=set_header(), proxies=proxy if gfw else None, cookies=cookies)
    except ConnectionResetError:
        print('ConnectionResetError')
        time.sleep(10)
        get_content(url)
    except http.client.IncompleteRead:
        print('http.client.IncompleteRead')
        time.sleep(10)
        get_content(url)


def get_ip():
    return requests.get('http://icanhazip.com/').text


def chrome_cookie_to_dict(cookie_str):
    result = dict()
    for cookie in cookie_str.split('; '):
        cookie = cookie.split('=')
        result[cookie[0]] = cookie[1]
    return result


if __name__ == '__main__':
    pass
