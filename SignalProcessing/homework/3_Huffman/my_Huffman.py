codebook = {'A':'10','B':'01','C':'110','D':'00','E':'111'}
uncodebook = dict((value,key) for key,value in codebook.items())

def write_huffman_code(uncodedata):
    codedata = ''
    for char in uncodedata:
        codedata += codebook[char]
    return codedata

def read_huffman_code(codedata):
    uncodedata = ''
    flag ,i = 0,0
    while i <= len(codedata):
        if codedata[flag:i] in uncodebook:
            uncodedata += uncodebook[codedata[flag:i]]
            flag = i
        i += 1
    return uncodedata

input = 'ACBDEAAABCDE'#input a String consists of A,B,C,D,E
print('Origin input:',input)
print('Encode huffman:',write_huffman_code(input))
print('Decode huffman:',read_huffman_code(write_huffman_code(input)))