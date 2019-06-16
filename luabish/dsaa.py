import random
from collections import deque
from functools import reduce

##############################数值#########################


def int_to_bin32(i):
    """
    将整数从python中的表示法转换成其他语言的32位整数表示\n
    i:十进制整数
    return : 该整数的32位表示形式
    """
    tmp_str = (bin(((1 << 32) - 1) & i)
               [2:]).zfill(32)  # str.zfill(x)用0补齐字符串，生成一个x位字符串
    return int(tmp_str, 2)


def get_digit_sum(num):
    """
    返回一个整数的各位数字之和
    """
    digits = [int(n) for n in str(num)]

    def add_all(x, y):
        return x + y
    return reduce(add_all, digits)
##############################列表#########################


def generate_matrix(strings, x, y):
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


def print_matrix(matrix):
    """
    打印二维矩阵，显示行数列数，并且每行之间会换行
    """
    x = len(matrix)
    y = len(matrix[0])
    print('\n-----{}*{}-----'.format(x, y))
    for i in range(x):
        print(matrix[i])
    print('-------------')


##############################栈###########################


class Stack():
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

    def __bool__(self):   # 使该类支持布尔测试：bool()函数先找__bool__,然后找__len__
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
            return self.items[len(self.items)-1]

    def get_size(self):
        return len(self.items)

##########################链表相关###################################


class LinkNode():  # 不加括号，不继承object也可以
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        return str(self.val)
    __str__ = __repr__


def linknode_has_circle(linknode):
    """
    判断单向链表是否有环
    """
    pass


def generate_linknode_from_list(content_list):
    last_node = None
    while content_list:
        this_node = LinkNode(content_list.pop())
        if not last_node:
            last_node = this_node
            continue
        this_node.next = last_node
        last_node = this_node
    return last_node


def generate_random_linknode(length, value_max):
    """
    生成一个length长度[1,N]的单向链表，值为[0,value_max]
    ;@return ;ListNode
    """
    last_node = None
    for i in range(length):
        this_value = random.randint(0, value_max)
        this_node = LinkNode(this_value)
        if i == 0:
            last_node = this_node
            if length == 1:
                return this_node
            continue
        if i == length-1:
            this_node.next = last_node
            return this_node
        this_node.next = last_node
        last_node = this_node


def print_linknode(node):
    """
    打印单项链表
    如果传入字符串，也可以打印字符串
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


def get_random_node(head):
    length = 0
    tmp = head
    while tmp:
        length += 1
        tmp = tmp.next
    if length > 0:
        random_index = random.randint(0, length)
    index = 0
    while head:
        if index == random_index:
            return head
        head = head.next
        index += 1


def get_specific_linknode(node, val):
    """
    遍历搜索第一个值为val的链表节点并返回，不存在将抛出异常
    """
    while node:
        if node.val == val:
            return node
        if node.next == None:
            raise ValueError('不存在值为%d的节点' % val)
        node = node.next


def linknode_add_circle(linknode, entry_point_value):
    """
    为单向链表增加一个环：连接尾节点到前面第一个值为entry_point_value的节点\n
    特殊情况说明：不能用尾巴节点链接自己。
    ;linknode;单项链表
    ;entry_point_value;与尾节点连起来的节点的值，以第一个遇到的节点为准
    """
    head = linknode
    entry_node = None
    while linknode:
        if linknode.val == entry_point_value:
            entry_node = linknode
        if linknode.next == None:
            if entry_node is linknode:
                raise ValueError('环不能指向尾巴节点')
            else:
                linknode.next = entry_node
                break
        linknode = linknode.next
    return head
##########################二叉树相关#################################


class TreeNode():
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.parent = None


def middle_order_inter(root):
    """
    中序遍历一颗二叉树
    """
    pass


def generate_treenode(input, with_parent=False):
    """
    层次遍历\n
    ;input; 1,2,null,3\n
    ;with_parent;是否为子树增加parent属性指向父节点，默认位False\n
    注意，null不需要全写出来。不存在的子树下面的null不需要写，只需要写有父节点的子节点\n
    """
    input = input.strip()
    if not input:
        return None

    inputValues = [s.strip() for s in input.split(',')]
    root = TreeNode(int(inputValues[0]))
    nodeQueue = [root]
    front = 0
    index = 1
    while index < len(inputValues):
        node = nodeQueue[front]
        front = front + 1

        item = inputValues[index]
        index = index + 1
        if item != "null":
            leftNumber = int(item)
            node.left = TreeNode(leftNumber)
            if with_parent:
                node.left.parent = node
            nodeQueue.append(node.left)

        if index >= len(inputValues):
            break

        item = inputValues[index]
        index = index + 1
        if item != "null":
            rightNumber = int(item)
            node.right = TreeNode(rightNumber)
            if with_parent:
                node.right.parent = node
            nodeQueue.append(node.right)
    return root


def print_treenode(node, prefix="", isLeft=True):
    if not node:
        print("Empty Tree")
        return

    if node.right:
        print_treenode(node.right, prefix +
                       ("│   " if isLeft else "    "), False)

    print(prefix + ("└── " if isLeft else "┌── ") + str(node.val))

    if node.left:
        print_treenode(node.left, prefix +
                       ("    " if isLeft else "│   "), True)


def get_specific_treenode(root, val):
    """
    广度优先搜索，返回在root二叉树中查找到的第一个值为val的节点
    """
    quene = deque([])
    quene.append(root)
    while quene:
        this_node = quene.popleft()
        if this_node.val == val:
            return this_node
        if this_node.left:
            quene.append(this_node.left)
        if this_node.right:
            quene.append(this_node.right)
    print('未能找到该值')
    return None


if __name__ == '__main__':
    print_matrix([[1, 2], [3, 4]])
