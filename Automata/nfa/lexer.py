from enum import Enum

class Token(Enum):
    EOS = 0
    END_OF_INPUT = 1
    ANY = 2
    L = 3
    SQUARE_START = 4
    SQUARE_END = 5
    OPEN_CURLY = 6
    CLOSE_CURLY = 7
    CLOSURE = 8
    PLUS_CLOSURE = 9
    DASH = 10
    OR = 11
    OPEN_PAREN = 12
    CLOSE_PAREN = 13

Tokens = {
    '.': Token.ANY,
    '(': Token.OPEN_PAREN,
    ')': Token.CLOSE_PAREN,
    '[': Token.SQUARE_START,
    ']': Token.SQUARE_END,
    '{': Token.OPEN_CURLY,
    '}': Token.CLOSE_CURLY,
    '*': Token.CLOSURE,
    '+': Token.PLUS_CLOSURE,
    '-': Token.DASH,
    '|': Token.OR,
}

"""
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

class Lexer(object):
    """
    对正则表达式进行解析，校验正则表达式是否合法，得到对应字符的Token,目前不支持转义字符的输入
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0
        self.current_text = ''
        self.current_token = None
        self.check_pattern()
        # self.del_paren() 
        # print(self.pattern) 

    def next(self):
        """
        返回当前对应的Tokens并读入下一个字符
        """
        pos = self.pos
        pattern = self.pattern
        if pos > len(pattern) - 1:
            self.current_token = Token.EOS
            return Token.EOS

        text = self.current_text = pattern[pos]
        self.current_token = self.get_token(text)
        # print(self.current_token)
        return self.current_token

    def get_token(self, text):
        """
        获取Tokens
        """
        self.pos = self.pos + 1
        return Tokens.get(text, Token.L)

    def check_pattern(self):
        """
        检查正则表达式括号是否匹配
        """
        brackets = ['(',')','[',']','{','}']
        cnt = [0,0,0,0,0,0]
        for i in range(len(self.pattern)):
            for j in range(len(brackets)):
                if self.pattern[i] == brackets[j]:
                    cnt[j] += 1
            if cnt[0] < cnt[1] or cnt[2] < cnt[3] or cnt[4] < cnt[5]:
                print('Error: Please check the input pattern')
                exit(0)
        if cnt[0] != cnt[1] or cnt[2] != cnt[3] or cnt[4] != cnt[5]:
            print('Error: Please check the input pattern')
            exit(0)

    def del_paren(self):
        cnt = 0
        for i in range(len(self.pattern)):
            if self.pattern[cnt] == '(' or self.pattern[cnt] == ')':
                self.pattern = self.pattern[:cnt] + self.pattern[cnt+1:]
                cnt -= 1
            cnt += 1

    def match(self, token):
        """
        将输入的token与当前的token进行比较
        """
        return self.current_token == token