# -*- coding: utf-8 -*-
import myre

# pattern : class
class_map={
    '0*1*' : 1,
    '1*0*' : 2,
}

def classify(string,class_map):
    for pattern in class_map:
        if myre.match(pattern, string):
            return class_map[pattern]
    return None

print('class_map:',class_map)
print('please input test string.')
while True:
    input_string = input('>>')
    print('class:',classify(input_string,class_map))
