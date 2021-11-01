"""
数值计算类工具函数
"""
from functools import reduce


def int_to_bin32(i):
    """
    将整数从python中的表示法转换成其他语言的32位整数表示\n
    i:十进制整数
    return : 该整数的32位表示形式
    """
    tmp_str = (bin(((1 << 32) - 1) & i)[2:]).zfill(32)  # str.zfill(x)用0补齐字符串，生成一个x位字符串
    return int(tmp_str, 2)


def get_digit_sum(num):
    """
    返回一个整数的各位数字之和
    """
    return reduce(lambda x, y: x + y, [int(n) for n in str(num)])
