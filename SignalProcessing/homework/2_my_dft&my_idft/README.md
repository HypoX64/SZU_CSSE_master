## my_dft &my_ idft
This code finish in python3 and use numpy as a  Matrix tool.
@Hypo,雷海波 1910273011
## test code
my_dft and my_ idft  codes were wrote in my_dft.py
In test.py , I compare my_dft/idft's result with np.fft.fft/ifft's result,and found they are same.
```shell
python test.py
```
result:
```shell
test1:
Xn: [1 2 3 4 5 6]
My:
DFT Xn with my_dft: [21.+0.j    -3.+5.196j -3.+1.732j -3.-0.j    -3.-1.732j -3.-5.196j]
IDFT my_Xk with my_idft: [1.-0.j 2.+0.j 3.-0.j 4.+0.j 5.+0.j 6.-0.j]
Numpy:
FFT Xn with np.fft.fft: [21.+0.j    -3.+5.196j -3.+1.732j -3.-0.j    -3.-1.732j -3.-5.196j]
IFFT np_Xk with np.fft.ifft: [1.-0.j 2.+0.j 3.-0.j 4.+0.j 5.-0.j 6.+0.j]

test2:
Xn: [1 1 1 1 1 1]
My:
DFT Xn with my_dft: [ 6.+0.j -0.-0.j  0.-0.j  0.-0.j -0.-0.j -0.-0.j]
IDFT my_Xk with my_idft: [1.-0.j 1.+0.j 1.-0.j 1.+0.j 1.+0.j 1.-0.j]
Numpy:
FFT Xn with np.fft.fft: [6.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j 0.+0.j]
IFFT np_Xk with np.fft.ifft: [1.+0.j 1.+0.j 1.+0.j 1.+0.j 1.+0.j 1.+0.j]
```

