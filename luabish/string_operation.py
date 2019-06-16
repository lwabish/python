

def get_middle_str(content, start, end):
    """
    将content字符串从start到end截取出来
    """
    start_index = content.index(start)
    if start_index >= 0:
        start_index += len(start)
    end_index = content.index(end)
    return content[start_index:end_index]


def remove_special_space(content):
    '''
    移除\xa0之类的特殊空格
    '''
    return "".join(content.split())
