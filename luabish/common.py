import datetime
import functools
import logging
import time


class Logger:
    pass


def Singleton(cls):
    """
    装饰器：修饰class，使得该类成为单例类
    """
    _instance = dict()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton


def print_used_time(func=None, show_params=True):
    """
    装饰器：可以打印出函数的执行时间
    ;show_params;默认会打印出函数的参数，在函数参数非常长时，可以给False禁用打印参数。
    ;同时支持提供参数或不提供参数
    ;example;
        @print_used_time
        @print_used_time(show_params=False)
    """
    def decorator(func):
        @functools.wraps(func)
        def clocked(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - t0
            name = func.__name__
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


def get_object_infos(obj, ret_type='p'):
    '''
    打印一个对象当前所有的属性名和属性值；如果可以len()，会一起打印
    ;@type;p：打印，不返回值。l：返回包含了一系列数据字典的列表
    '''
    infos = list()
    for attr in dir(obj):
        value = getattr(obj, attr)
        try:
            length = ' [长度:{}]'.format(len(value))
        except:
            length = ''
        info = dict()
        info['attr'], info['len'], info['v'] = attr, length, value
        infos.append(info)

    if ret_type == 'p':
        for info in infos:
            print(info['attr']+info['len']+' -->>> '+str(info['v'])+'\n')
    elif ret_type == 'l':
        return infos


def prettiefy_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
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
                if len(obj) == 1:
                    yield '{%s: %s}' % (k, v)
                else:
                    yield '{%s: %s,\n' % (k, v)
            elif i == len(obj) - 1:  # 结尾,拼右花括号
                yield '%s%s: %s}' % (indent, k, v)
            else:  # 中间
                yield '%s%s: %s,\n' % (indent, k, v)
    return ''.join(_pretty(obj, indent))


def transform_time(data, target_type):
    """
    将data转换为target_type的时间类型
    时间戳只能由time obj转换
    ;param data;要转换的原始数据
    ;param target_type;
        1: string
        2: timestamp
        3: time tuple(time obj)
        4: datetime tuple(datetime obj)
    ;return;
        以target_type为格式的时间对象

    >>> from my_universal_operation import transform_time
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
    if isinstance(data, str):
        if target_type == 2:  # string 转 时间戳
            _time_obj = transform_time(data, 3)  # string 先转 time obj
            result = transform_time(_time_obj, 2)  # time obj转时间戳
        elif target_type == 3:  # string 转 time obj
            result = time.strptime(data, "%Y-%m-%d %H:%M:%S")
        elif target_type == 4:  # string 转datetime obj
            result = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
    elif isinstance(data, float):
        if target_type == 1:  # 时间戳转字符串
            _time_obj = transform_time(data, 3)
            result = transform_time(_time_obj, 1)
        elif target_type == 3:  # 时间戳转time obj
            result = time.localtime(data)
        elif target_type == 4:  # 时间戳转datetime obj
            result = datetime.datetime.fromtimestamp(data)
    elif isinstance(data, tuple):
        if target_type == 1:  # time obj转字符串
            result = time.strftime("%Y-%m-%d %H:%M:%S", data)
        elif target_type == 2:  # time obj转时间戳
            result = time.mktime(data)
        elif target_type == 4:  # time obj转datetime obj
            result = datetime.datetime(*data[0:6])
    elif isinstance(data, datetime.datetime):
        if target_type == 1:  # datetime obj转string
            result = data.strftime("%Y-%m-%d %H:%M:%S")
        elif target_type == 2:  # datetime obj转时间戳
            _time_obj = transform_time(data, 3)
            result = transform_time(_time_obj, 2)
        elif target_type == 3:  # datetime obj转time obj
            result = data.timetuple()
    else:
        print(type(data))
        print('不支持的数据类型')
    return result


def sort_dict(data: dict, reverse=False):
    return {key: data[key] for key in sorted(data, reverse=reverse)}


if __name__ == '__main__':
    # do doctests
    import doctest
    doctest.testmod(verbose=True)