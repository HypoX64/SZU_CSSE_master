from .cell import EPSILON,CCL

def match(input_string, start_node):
    """匹配字符串
    input_string :: 需要配备的字符串
    start_node   :: NFA起始节点
    return       :: True | False
    """

    # 初始化运行状态的状态集合: 起始节点+空转移能到达的节点
    current_state_set = [start_node] 
    next_state_set = closure(current_state_set)

    # 循环读入字符生成状态集合
    for i, ch in enumerate(input_string):
        # 读入一个字符后的状态集合+空转移能到达的节点
        current_state_set = move(next_state_set, ch)
        next_state_set = closure(current_state_set)

        # 状态集合为空,返回False
        if next_state_set is None:
            return False

        # 读入最后一个字符且存在接受状态的返回True
        if has_accepted_state(next_state_set) and i == len(input_string) - 1:
            return True

    return False


def closure(state_set):
    if len(state_set) <= 0:
        return None

    node_stack = []
    for i in state_set:
        node_stack.append(i)

    while len(node_stack) > 0:
        node = node_stack.pop()
        next1 = node.next_1
        next2 = node.next_2
        if next1 is not None and node.edge == EPSILON:
            if next1 not in state_set:
                state_set.append(next1)
                node_stack.append(next1)

        if next2 is not None and node.edge == EPSILON:
            if next2 not in state_set:
                state_set.append(next2)
                node_stack.append(next2)
        
    return state_set


def move(state_set, ch):
    out_set = []
    for node in state_set:
        if node.edge == CCL and ch in node.char_set:
            out_set.append(node.next_1)
    return out_set


def has_accepted_state(state_set):
    for state in state_set:
        if state.next_1 is None and state.next_2 is None:
            return True