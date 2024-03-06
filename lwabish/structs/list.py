"""
数组、队列、栈相关的数据结构和工具函数
"""


def new_matrix(strings, x, y):
    """
    由字符串顺序生成二维矩阵\n
    """
    if x * y != len(strings):
        return '元素数不匹配'
    result_mat = [[''] * y for i in range(x)]
    strings = list(strings)
    strings.reverse()
    # print(strings)
    for i in range(len(result_mat)):
        for j in range(len(result_mat[i])):
            # print(i, j)
            result_mat[i][j] = strings.pop()
    return result_mat


class Stack:
    """
    用列表实现栈\n
    Stack()    建立一个空的栈对象\n
    add()     入栈\n
    pop()      出栈\n
    peek()     返回最顶层的元素，不删除\n
    is_empty() 栈是否为空\n
    get_size() 返回栈中元素的个数\n
    """

    def __init__(self):
        self.items = []

    def __bool__(self):  # 使该类支持布尔测试：bool()函数先找__bool__,然后找__len__
        if self.items:
            return True
        else:
            return False

    def is_empty(self):
        return len(self.items) == 0

    def add(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items) - 1]

    def get_size(self):
        return len(self.items)
