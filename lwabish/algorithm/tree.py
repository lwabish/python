"""
树相关数据结构和算法
"""


class TreeNode:
    def __init__(self, x):
        """
        :param x: 二叉树节点的值
        :return 一个二叉树节点
        """
        self.val = x
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self) -> str:
        return 'TreeNode[{}]'.format(str(self.val))

    def __repr__(self) -> str:
        return 'TreeNode[{}]'.format(str(self.val))


def new_tree(values: str, with_parent=False):
    """
    根据层次遍历字符串生成一颗二叉树，分隔符为英文逗号，空节点用字符串null表示\n
    注意：null不需要全写出来。不存在的子树下面的null不需要写\n
    :param values: 层次遍历字符串。例如 "1,2,null,3"
    :param with_parent: 是否包含指向父节点的属性
    :return: 二叉树的根节点
    """
    value_str = values.strip()
    if not value_str:
        return None
    values = [s.strip() for s in value_str.split(',')]

    root = TreeNode(int(values[0]))
    # 初始化工作队列，把根节点放进去
    node_queue = [root]
    # 工作队列待处理的节点索引
    front = 0
    # 新构造的TreeNode的值索引
    index = 1

    while index < len(values):
        # 从工作队列中取出父节点
        node = node_queue[front]
        front = front + 1

        # 给当前的父节点装配左子树
        value = values[index]
        index = index + 1
        if value != "null":
            left = int(value)
            node.left = TreeNode(left)
            if with_parent:
                node.left.parent = node
            node_queue.append(node.left)

        if index >= len(values):
            break

        # 给当前的父节点装配右子树
        value = values[index]
        index = index + 1
        if value != "null":
            right = int(value)
            node.right = TreeNode(right)
            if with_parent:
                node.right.parent = node
            node_queue.append(node.right)
    return root


def print_tree(root: TreeNode, prefix="", is_left=True):
    """
    在控制台打印一颗二叉树，方便肉眼观察
    :param root: 根节点
    :param prefix: 递归参数
    :param is_left: 递归参数
    :return: 无
    """
    if not root:
        print("空🌲")
        return
    if root.right:
        print_tree(root.right, prefix + ("│   " if is_left else "    "), False)
    print(prefix + ("└── " if is_left else "┌── ") + str(root.val))
    if root.left:
        print_tree(root.left, prefix + ("    " if is_left else "│   "), True)


if __name__ == '__main__':
    print(TreeNode(1))
