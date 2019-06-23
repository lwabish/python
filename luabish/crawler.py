import random as _random
import requests as _requests
import http as _http
import time as _time
from requests_html import HTMLSession as _HTMLSession
from urllib3.util import Retry as _Retry
from requests.adapters import HTTPAdapter as _HTTPAdapter
from http.client import IncompleteRead as _IncompleteRead
from lxml import etree as _etree

UAS = [
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
PROXY = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080',
}


def get_fund_value(id: str) -> float:
    url = 'http://fund.eastmoney.com/{}.html'.format(id)
    html = _etree.HTML(get_content(url).text)
    return float(html.xpath('//*[@id="gz_gsz"]/text()')[0])


def set_header():
    random_ip = str(_random.randint(0, 255)) + '.' + str(_random.randint(0, 255)) + '.' + str(
        _random.randint(0, 255)) + '.' + str(_random.randint(0, 255))
    headers = {
        'User-Agent': _random.choice(UAS),
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        'X-Forwarded-For': random_ip,
    }
    return headers


def build_session(gfw=False, cookies=None, rq_html=False):
    if rq_html:
        s = _HTMLSession()
    else:
        s = _requests.Session()
    s.headers = set_header()
    s.proxies = PROXY if gfw else None
    s.cookies = _requests.utils.cookiejar_from_dict(
        cookies) if cookies else _requests.utils.cookiejar_from_dict({})
    retries = _Retry(total=5, backoff_factor=10,
                     status_forcelist=[500, 502, 503, 504])
    s.mount('http://', _HTTPAdapter(max_retries=retries))
    return s


def get_content(url, gfw=False, cookies=None, **kwargs):
    """
    服务器错误时重试+随机header
    """
    try:
        s = _requests.Session()

        retries = _Retry(total=5, backoff_factor=10,
                         status_forcelist=[500, 502, 503, 504])
        s.mount('http://', _HTTPAdapter(max_retries=retries))
        return s.get(url, headers=set_header(), proxies=PROXY if gfw else None, cookies=cookies, **kwargs)
    except ConnectionResetError:
        print('ConnectionResetError')
        _time.sleep(10)
        get_content(url)
    except _http.client.IncompleteRead:
        print('http.client.IncompleteRead')
        _time.sleep(10)
        get_content(url)


def get_header(url, gfw=False, cookies=None):
    try:
        s = _requests.Session()
        return s.head(url, headers=set_header(), proxies=PROXY if gfw else None, cookies=cookies)
    except Exception as e:
        print(e)


def get_ip():
    return _requests.get('http://icanhazip.com/').text


def chrome_cookie_to_dict(cookie_str):
    result = dict()
    for cookie in cookie_str.split('; '):
        cookie = cookie.split('=')
        result[cookie[0]] = cookie[1]
    return result


if __name__ == '__main__':
    print(get_content('http://91porn.com/my_profile.php', True,
                      allow_redirects=False).status_code)
