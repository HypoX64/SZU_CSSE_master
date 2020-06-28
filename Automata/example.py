import myre
"""
规则：
"."       : 用于匹配任意单个字符
"[a-z]"   : 匹配a-z中的任意单个字符
"{a,b,c}" : 匹配a或b或c中的任意单个字符，也可以写作(a|b|c)
"*"       : 闭包
"+"       : 正闭包
"|"       : 或(加)
""        : 默认进行连接操作(乘)
"""

# test 1
#至少含两个连续0的0、1串组成的语言
pattern = '(0|1)*00(0|1)*'
st1 = '01111011101'
st2 = '011110011101'
print('test 1:',myre.match(pattern, st1),myre.match(pattern, st2))

# test 2 
# 开头字符与尾字符相同都是0或1
pattern = '(1(0|1)*1|0(0|1)*0)'
st1 = '01111011101'
st2 = '011110011100'
print('test 2:',myre.match(pattern, st1),myre.match(pattern, st2))

# test 3 
# 仅由'a'或'b'或'c'字符构成
st1 = 'sakfhsrfefh'
st2 = 'abababababaaccccbaaaaabbababaaaa'
pattern = '[a-c]*' # 或者 (a|b|c) 或者{a,b,c}* 
print('test 3:',myre.match(pattern, st1),myre.match(pattern, st2))

# test 4 
# 包含'hypo'的字符串
st1 = 'sakfhypssdesrfefh'
st2 = 'sahypossdesrfefhhypoasd'
pattern = '.*(hypo)+.*' # 或者{a,b}*
print('test 4:',myre.match(pattern, st1),myre.match(pattern, st2))

# test 5
# 极限操作，我也不知道这是啥
st1 = 'sakfasdasd324228435'
st2 = 'Shenzhen University'
pattern = '((((s.*n|a)+)*)+{a,x}*|.* *.*|[a-z]*)*****'
print('test 5:',myre.match(pattern, st1),myre.match(pattern, st2))
