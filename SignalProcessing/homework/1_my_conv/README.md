## my_conv
This code finish in python3 and use numpy as a  Matrix tool.
@Hypo,雷海波 1910273011
## to  test code
In test.py , I compare my_conv's result with np.convolve's result,and found they are same.
```shell
python test.py
```
result:
```shell
test1:
conv with my_conv: [ 1.  2.  4.  7. 10. 13.  9. 11.  6.]
conv with np.convolve: [ 1  2  4  7 10 13  9 11  6]
test2:
conv with my_conv: [0.3319973  0.68744623 0.39637609 0.44753119 0.53135132 0.17920317
 0.22541965 0.26269674 0.03181879]
conv with np.convolve: [0.3319973  0.68744623 0.39637609 0.44753119 0.53135132 0.17920317
 0.22541965 0.26269674 0.03181879]
[Finished in 0.2s]
```

