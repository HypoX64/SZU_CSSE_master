# -*- coding: utf-8 -*-
import myre

# 读取txt
f = open('./input.txt', 'r', encoding='utf-8')
input_txt = f.read()
f.close()

# 将txt分割为单词
input_strings = myre.split(input_txt, [' ',',','"','.','(',')'])

pattern = 's{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}*n'
# 或者 pattern = 's[a-z]*n'
myre.match
for string in input_strings:
    if myre.match(pattern, string.lower()):
        print(string)
