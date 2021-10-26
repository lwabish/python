import datetime
import functools
import logging
import time

import requests


def send_wx_notification(secret_key: str, title: str, content: str) -> bool:
    """使用Server酱向微信推送消息
    只能实现单点推送，没有订阅机制
    ref: http://sc.ftqq.com/
    """
    sc_api = 'https://sc.ftqq.com/{}.send'.format(secret_key)
    if requests.post(sc_api, data={'text': title, 'desp': content}).status_code == 200:
        return True
    else:
        return False


def singleton(cls):
    """装饰器：修饰class，使得该类成为单例类
    """
    _instance = dict()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


def print_used_time(func=None, show_params=True):
    """装饰器：打印出函数的执行时间

    show_params(O): 打印出函数的参数，默认True

    example:
        @print_used_time
        Class A:
            pass

        @print_used_time(show_params=False)
        Class A:
            pass
    """

    def decorator(f):
        @functools.wraps(f)
        def clocked(*args, **kwargs):
            t0 = time.time()
            result = f(*args, **kwargs)
            elapsed = time.time() - t0
            name = f.__name__
            if show_params:
                arg_list = list()
                if args:
                    # obj==eval(repr(obj)),str()函数将对象转为字符串后不一定可逆
                    arg_list.append(','.join(repr(arg) for arg in args))
                if kwargs:
                    pairs = ['%s=%r' % (k, w)
                             for k, w in sorted(kwargs.items())]
                    arg_list.append(','.join(pairs))
                    # print(arg_list)
                arg_str = ','.join(arg_list)
                print('[%0.8fs] %s(%s) -> %r' %
                      (elapsed, name, arg_str, result))
            else:
                print('[%0.8fs] %s() -> %r' % (elapsed, name, result))
            # print(show_params)
            return result

        return clocked

    if func:
        return decorator(func)
    else:
        return decorator


def get_object_infos(obj, ret_type: str = 'p'):
    """打印一个对象当前所有的属性名和属性值
    如果可以调用len()，会一起打印其length

    type: p-打印，不返回值。
             l-返回包含一系列数据字典的列表
    """
    infos = list()
    for attr in dir(obj):
        value = getattr(obj, attr)
        try:
            length = ' [长度:{}]'.format(len(value))
        except TypeError:
            length = ''
        info = dict()
        info['attr'], info['len'], info['v'] = attr, length, value
        infos.append(info)

    if ret_type == 'p':
        for info in infos:
            print(info['attr'] + info['len'] + ' -->>> ' + str(info['v']) + '\n')
    elif ret_type == 'l':
        return infos


def beautify_dict(obj, init_indent=' '):
    """以易读的形式打印字典
    """

    def _pretty(o, indent):
        for i, tup in enumerate(o.items()):
            k, v = tup
            # 如果是字符串则拼上""
            if isinstance(k, str):
                k = '"%s"' % k
            if isinstance(v, str):
                v = '"%s"' % v
            # 如果是字典则递归
            if isinstance(v, dict):
                # 计算下一层的indent
                v = ''.join(_pretty(v, indent + ' ' * len(str(k) + ': {')))
            # case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:  # 开头,拼左花括号
                if len(o) == 1:
                    yield '{%s: %s}' % (k, v)
                else:
                    yield '{%s: %s,\n' % (k, v)
            elif i == len(o) - 1:  # 结尾,拼右花括号
                yield '%s%s: %s}' % (indent, k, v)
            else:  # 中间
                yield '%s%s: %s,\n' % (indent, k, v)

    return ''.join(_pretty(obj, init_indent))


def transform_time(date, target_type):
    """将date转换为target_type的时间类型
    时间戳只能由time obj转换

    ;param data;要转换的原始数据
    ;param target_type int;
        1: string
        2: timestamp
        3: time tuple(time obj)
        4: datetime tuple(datetime obj)
    ;return;
        以target_type为格式的时间对象

    >>> from lwabish.common import transform_time
    >>> date_str = '2019-02-01 22:22:22'
    >>> time_stamp = 1549030942.0
    >>> time_obj = (2019,2,1,22,22,22,4,32,-1)
    >>> dt_obj = datetime.datetime(2019,2,1,22,22,22)

    >>> transform_time(date_str,2)
    1549030942.0
    >>> transform_time(date_str,3)
    time.struct_time(tm_year=2019, tm_mon=2, tm_mday=1, tm_hour=22, tm_min=22, tm_sec=22, tm_wday=4, tm_yday=32, tm_isdst=-1)
    >>> transform_time(date_str,4)
    datetime.datetime(2019, 2, 1, 22, 22, 22)

    >>> transform_time(time_stamp,1)
    '2019-02-01 22:22:22'
    >>> transform_time(time_stamp,3)
    time.struct_time(tm_year=2019, tm_mon=2, tm_mday=1, tm_hour=22, tm_min=22, tm_sec=22, tm_wday=4, tm_yday=32, tm_isdst=0)
    >>> transform_time(time_stamp,4)
    datetime.datetime(2019, 2, 1, 22, 22, 22)

    >>> transform_time(time_obj,1)
    '2019-02-01 22:22:22'
    >>> transform_time(time_obj,2)
    1549030942.0
    >>> transform_time(time_obj,4)
    datetime.datetime(2019, 2, 1, 22, 22, 22)

    >>> transform_time(dt_obj,1)
    '2019-02-01 22:22:22'
    >>> transform_time(dt_obj,2)
    1549030942.0
    >>> transform_time(dt_obj,3)
    time.struct_time(tm_year=2019, tm_mon=2, tm_mday=1, tm_hour=22, tm_min=22, tm_sec=22, tm_wday=4, tm_yday=32, tm_isdst=-1)
    """
    result = None
    if isinstance(date, str):
        if target_type == 2:  # string 转 时间戳
            _time_obj = transform_time(date, 3)  # string 先转 time obj
            result = transform_time(_time_obj, 2)  # time obj转时间戳
        elif target_type == 3:  # string 转 time obj
            result = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        elif target_type == 4:  # string 转datetime obj
            result = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            raise Exception('target_type为整数类型，请查看参数说明')
    elif isinstance(date, float):
        if target_type == 1:  # 时间戳转字符串
            _time_obj = transform_time(date, 3)
            result = transform_time(_time_obj, 1)
        elif target_type == 3:  # 时间戳转time obj
            result = time.localtime(date)
        elif target_type == 4:  # 时间戳转datetime obj
            result = datetime.datetime.fromtimestamp(date)
        else:
            raise Exception('target_type为整数类型，请查看参数说明')
    elif isinstance(date, tuple):
        if target_type == 1:  # time obj转字符串
            result = time.strftime("%Y-%m-%d %H:%M:%S", date)
        elif target_type == 2:  # time obj转时间戳
            result = time.mktime(date)
        elif target_type == 4:  # time obj转datetime obj
            result = datetime.datetime(*date[0:6])
        else:
            raise Exception('target_type为整数类型，请查看参数说明')
    elif isinstance(date, datetime.datetime):
        if target_type == 1:  # datetime obj转string
            result = date.strftime("%Y-%m-%d %H:%M:%S")
        elif target_type == 2:  # datetime obj转时间戳
            _time_obj = transform_time(date, 3)
            result = transform_time(_time_obj, 2)
        elif target_type == 3:  # datetime obj转time obj
            result = date.timetuple()
        else:
            raise Exception('target_type为整数类型，请查看参数说明')
    else:
        raise Exception('不受支持的data参数类型{}'.format(type(date)))
    return result


def sort_dict(data: dict, reverse=False):
    return {key: data[key] for key in sorted(data, reverse=reverse)}


class Logger:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    logger = None

    def __init__(self, file_path=None, level='debug',
                 fmt='%(asctime)s - [%(levelname)s]: %(message)s'):
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level_relations[level])
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(stream_handler)

        if file_path:
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(logging.Formatter(fmt))
            self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    # do doctests
    import doctest

    doctest.testmod(verbose=True)
