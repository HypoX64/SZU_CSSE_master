from nfa import builder,run

def match(pattern_string,input_string):
    """对input_string使用pattern_string进行正则匹配
    pattern_string :: 正则表达式
    input_string   :: 需要匹配的字符串
    return         :: True | False
    
    --------------------------------------------------------
    对应所支持的语法：
    "."       : 用于匹配任意单个字符
    "c"       : 匹配除了Token以外的输入的字符
    "[a-z]"   : 匹配a-z中的任意单个字符
    "{a,b,c}" : 匹配a或b或c中的任意单个字符，也可以写作(a|b|c)
    "*"       : 闭包
    "+"       : 正闭包
    "|"       : 或(加)
    ""        : 默认进行连接操作(乘)
    "("expr")": 支持使用括号提高运算优先级
    """
    nfa_start_node = builder.create_nfa(pattern_string)
    return run.match(input_string, nfa_start_node)            

def split(string,keys):
    """
    string  ::  需要分割的字符
    keys    ::  分割关键字 eg. keys = [' ',',','"','.','(',')']
    return  ::  分割后的字符串数组
    """
    out_strings = []
    cnt = 0
    for i in range(len(string)):
        if string[i] in keys:
            if cnt != i:
                out_strings.append(string[cnt:i])
            cnt = i+1
    return out_strings
