# -*- coding: utf-8 -*-
from .lexer import Lexer,Token
from .cell import Cell,PairCell,EPSILON,CCL,EMPTY

lexer = None

def create_nfa(pattern_string):
    """NFA自动机创建入口
    pattern_string  :: RE表达式
    return          :: nfa起始节点
    """
    global lexer
    lexer = Lexer(pattern_string)
    lexer.next()
    nfa_cells_final = PairCell()
    expr(nfa_cells_final)
    return nfa_cells_final.start_node

"""
词法分析按照优先级自顶向下
expr ::= <factor_connect> ("|" factor_connect)*                                  # "|" 加（或）
factor_connect ::= factor | factor factor*                                       # "" 乘（直接连接）
factor ::= term | term ("*"|"+")*                                               # "*"闭包  "+"正闭包
term ::= char | group | "[" char "-" char "]" | "{" char "," char "}" | "."      # 基本单元,终止符
group ::= "("expr")"                                                             # 递归解决括号优先级
"""

def group(nfa_cells):
    """
    递归调用expr(),实现()操作
    """
    if lexer.match(Token.OPEN_PAREN):
        lexer.next()
        expr(nfa_cells)
    if lexer.match(Token.CLOSE_PAREN):
        lexer.next()
    return True

def term(nfa_cells):
    """
    对 . | a (单个字符) | 单个一定范围[a-z]的字符 | {a,b,c} 某些字符集合中的单个字符->相当于(a+b+c)
    """
    if lexer.match(Token.L):             # char
        nfa_single_char(nfa_cells)
    elif lexer.match(Token.ANY):         # .
        nfa_any_single_char(nfa_cells)
    elif lexer.match(Token.CCL_START):   # [" char "-" char "]
        nfa_range_single_char(nfa_cells)
    elif lexer.match(Token.OPEN_CURLY):  # "{" char "," char "}"
        nfa_set_single_char(nfa_cells)
    elif lexer.match(Token.OPEN_PAREN):  # "("expr")"
        group(nfa_cells)

def factor(nfa_cells):
    """
    实现两种闭包 "*" | "+"
    """
    term(nfa_cells)
    if lexer.match(Token.CLOSURE) or lexer.match(Token.PLUS_CLOSURE):
        nfa_closure(nfa_cells)

def factor_connect(nfa_cells):
    """
    实现乘操作，即连接
    """
    if is_connect_token(lexer.current_token):
        factor(nfa_cells)
    
    while is_connect_token(lexer.current_token):
        new_cells = PairCell()
        factor(new_cells)
        nfa_cells.end_node.next_1 = new_cells.start_node
        nfa_cells.end_node = new_cells.end_node

    return True


def expr(nfa_cells):
    """
    实现OR操作
    """
    factor_connect(nfa_cells) # 第一支路
    
    new_cells = PairCell() # 其他支路
    while lexer.match(Token.OR):
        lexer.next()
        factor_connect(new_cells)

        start = Cell()
        start.next_1 = new_cells.start_node
        start.next_2 = nfa_cells.start_node
        nfa_cells.start_node = start

        end = Cell()
        new_cells.end_node.next_1 = end
        nfa_cells.end_node.next_2 = end
        nfa_cells.end_node = end

    return True

def nfa_single_char(nfa_cells):
    """
    L 匹配单个字符
    """
    if not lexer.match(Token.L):
        return False

    start = nfa_cells.start_node = Cell()
    nfa_cells.end_node = nfa_cells.start_node.next_1 = Cell()
    
    start.edge = CCL
    start.char_set = set()
    start.char_set.add(lexer.current_text)
    
    lexer.next()
    return True

def nfa_any_single_char(nfa_cells):
    """
    . 匹配任意单个字符
    """
    if not lexer.match(Token.ANY):
        return False

    start = nfa_cells.start_node = Cell()
    nfa_cells.end_node = nfa_cells.start_node.next_1 = Cell()
    
    start.edge = CCL
    start.char_set = set()
    for i in range(127):
        start.char_set.add(chr(i))

    lexer.next()
    return False

def nfa_range_single_char(nfa_cells):
    """
    [a-z] 匹配范围字符集
    """
    if not lexer.match(Token.CCL_START):
        return False
    lexer.next()
    start = nfa_cells.start_node = Cell()
    start.next_1 = nfa_cells.end_node = Cell()

    start.edge = CCL

    # get range char set
    first = ''
    while not lexer.match(Token.CCL_END):
        if not lexer.match(Token.DASH):
            first = lexer.current_text
            start.char_set.add(first)
        else:
            lexer.next()
            for c in range(ord(first), ord(lexer.current_text) + 1):
                start.char_set.add(chr(c))
        lexer.next()

    lexer.next()
    return True

def nfa_set_single_char(nfa_cells):
    """
    {a,b,c....} 匹配字符集 相当于(a|b|c...)
    """
    if not lexer.match(Token.OPEN_CURLY):
        return False

    lexer.next()
    start = nfa_cells.start_node = Cell()
    start.next_1 = nfa_cells.end_node = Cell()
    start.edge = CCL

    while not lexer.match(Token.CLOSE_CURLY):
        if lexer.current_text != ',':
            start.char_set.add(lexer.current_text)
        lexer.next()
    lexer.next()
    return True
 
def nfa_closure(nfa_cells):
    """
    * 闭包操作   以及  + 正闭包操作
    """
    if (not lexer.match(Token.CLOSURE)) and (not lexer.match(Token.PLUS_CLOSURE)):
        return False

    start = Cell()
    end = Cell()
    start.next_1 = nfa_cells.start_node
    if lexer.match(Token.CLOSURE): # +
        start.next_2 = end  # 连接start与end形成shortcut

    nfa_cells.end_node.next_1 = nfa_cells.start_node
    nfa_cells.end_node.next_2 = end

    nfa_cells.start_node = start
    nfa_cells.end_node = end

    lexer.next()
    return True

def is_connect_token(token):
    no_connect = [
        Token.CLOSE_PAREN,
        Token.EOS,
        Token.CLOSURE,
        Token.PLUS_CLOSURE,
        Token.CLOSE_CURLY,
        Token.CCL_END,
        Token.OR,
    ]
    return token not in no_connect
