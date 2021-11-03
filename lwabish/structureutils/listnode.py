"""
链表相关的数据结构和工具函数
"""
from random import randint
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        """
        :param val: 链表节点值
        """
        self.val = val
        self.next = next

    def __repr__(self):
        return 'ListNode[{}]'.format(str(self.val))

    __str__ = __repr__


def new_listnode(values: List) -> Optional[ListNode]:
    """
    根据数组值生成一个新链表
    :param values: 包含链表所有节点值的列表，正序
    :return: 头结点
    """
    # 存储上一个节点
    last_node = None
    while values:
        # 构造出本轮新的节点
        # 注意pop是从列表尾巴上弹出，因此是倒序组装
        this_node = ListNode(values.pop())
        this_node.next, last_node = last_node, this_node
    return last_node


def print_listnode(node: ListNode) -> None:
    """
    打印单项链表
    如果传入字符串，也可以打印字符串
    @:param node: 链表头结点
    """
    if type(node) == str:
        print(node)
        return
    while node and node.next:
        print(str(node.val) + "->", end='')
        node = node.next
    if node:
        print(node.val)
    else:
        print("Empty LinkedList")


def new_random_listnode(length: int, ceiling: int) -> Optional[ListNode]:
    """
    生成一个长度为length的单向链表，每个节点值为[0,value_max]中的随机整数
    @:param length: 长度
    @:param ceiling: 随机数上限
    @:return 头结点
    """
    last_node = None
    for i in range(length):
        this_value = randint(0, ceiling)
        this_node = ListNode(this_value)
        if i == 0:
            last_node = this_node
            if length == 1:
                return this_node
            continue
        if i == length - 1:
            this_node.next = last_node
            return this_node
        this_node.next, last_node = last_node, this_node


def get_random_node(head: ListNode) -> ListNode:
    """
    从链表中随机取一个node
    :param head: 头结点
    :return:
    """
    length = 0
    tmp = head
    while tmp:
        length += 1
        tmp = tmp.next
    random_index = randint(0, length)
    index = 0
    while head:
        if index == random_index:
            return head
        head = head.next
        index += 1


def get_first_node_by_value(node: ListNode, val: int) -> Optional[ListNode]:
    """
    遍历搜索第一个值为val的链表节点并返回
    :param node: 头结点
    :param val: 目标值
    :return: 目标节点或None
    """
    while node:
        if node.val == val:
            return node
        if node.next is None:
            return None
        node = node.next


def add_circle_for_listnode(node: ListNode, entry_point_value) -> ListNode:
    """
    为单向链表增加一个环：连接尾节点到正序遍历第一个值为entry_point_value的节点\n
    不能用尾巴节点链接自己。
    @:param node: 头结点
    @:param entry_point_value: 被尾节点链接成环目标节点的值
    @:return node: 原头结点
    """
    head = node
    entry_node = None
    while node:
        if node.val == entry_point_value:
            entry_node = node
        if node.next is None:
            if entry_node is node:
                raise ValueError('环不能指向尾巴节点')
            else:
                node.next = entry_node
                break
        node = node.next
    return head
