import numpy as np
import my_dft
'''
@Hypo 1910273011
A code to test my_dft and my_idft
'''

print('test1:')
Xn = np.array([1,2,3,4,5,6]) #change test vectors here
my_Xk = my_dft.dft(Xn)
my_Xn = my_dft.idft(my_Xk)
np_Xk = np.fft.fft(Xn)
np_Xn = np.fft.ifft(np_Xk)

print('Xn:',Xn)
print('My:\nDFT Xn with my_dft:',np.around(my_Xk,3))
print('IDFT my_Xk with my_idft:',np.around(my_Xn,3))
print('Numpy:\nFFT Xn with np.fft.fft:',np.around(np_Xk,3))
print('IFFT np_Xk with np.fft.ifft:',np.around(np_Xn,3))

print('\ntest2:')
Xn = np.array([1,1,1,1,1,1])
my_Xk = my_dft.dft(Xn)
my_Xn = my_dft.idft(my_Xk)
np_Xk = np.fft.fft(Xn)
np_Xn = np.fft.ifft(np_Xk)

print('Xn:',Xn)
print('My:\nDFT Xn with my_dft:',np.around(my_Xk,3))
print('IDFT my_Xk with my_idft:',np.around(my_Xn,3))
print('Numpy:\nFFT Xn with np.fft.fft:',np.around(np_Xk,3))
print('IFFT np_Xk with np.fft.ifft:',np.around(np_Xn,3))

