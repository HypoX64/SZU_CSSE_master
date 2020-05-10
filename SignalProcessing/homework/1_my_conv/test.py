import numpy as np
import my_conv
'''
@Hypo 1910273011
A code to test my_conv
'''

print('test1:')
x = np.array([1,0,1,1])
y = np.array([1,2,3,4,5,6])
out_my_conv = my_conv.conv(x, y)
out_np_conv  = np.convolve(x, y)
print('conv with my_conv:',out_my_conv)
print('conv with np.convolve:',out_np_conv)

print('test2:')
x = np.random.rand(3)
y = np.random.rand(7)
out_my_conv = my_conv.conv(x, y)
out_np_conv  = np.convolve(x, y)
print('conv with my_conv:',out_my_conv)
print('conv with np.convolve:',out_np_conv)