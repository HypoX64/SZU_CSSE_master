#边的类型
EPSILON = -1   # edge = EPSILON 对应的节点有两个出去的ε边
CCL     = -2   # edge = CCL     边对应的是字符集(包括单个字符) ，需要结合属性char_set
EMPTY   = -3   # edge = EMPTY   一条ε边

class Cell(object):

    def __init__(self):
        self.edge = EPSILON
        self.next_1 = None
        self.next_2 = None
        self.char_set = set()

class PairCell(object):
    """
    一对Cell的两个节点
    """
    def __init__(self):
        self.start_node = None
        self.end_node = None