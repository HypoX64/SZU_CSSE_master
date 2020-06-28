from enum import Enum

class Token(Enum):
    EOS = 0
    END_OF_INPUT = 1
    ANY = 2
    L = 3
    CCL_START = 4
    CCL_END = 5
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
    '[': Token.CCL_START,
    ']': Token.CCL_END,
    '{': Token.OPEN_CURLY,
    '}': Token.CLOSE_CURLY,
    '*': Token.CLOSURE,
    '+': Token.PLUS_CLOSURE,
    '-': Token.DASH,
    '|': Token.OR,
}

class Lexer(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0
        self.current_text = ''
        self.current_token = None
        # self.del_paren() 
        # print(self.pattern) 

    def next(self):
        """
        返回Token并读入下一个字符
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

    def del_paren(self):
        cnt = 0
        for i in range(len(self.pattern)):
            if self.pattern[cnt] == '(' or self.pattern[cnt] == ')':
                self.pattern = self.pattern[:cnt] + self.pattern[cnt+1:]
                cnt -= 1
            cnt += 1

    def match(self, token):
        return self.current_token == token