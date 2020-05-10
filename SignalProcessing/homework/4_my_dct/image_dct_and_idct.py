import numpy as np
import cv2

def block_dct_and_idct(g,QF):
    Q = np.array([[8,16,19,22,26,27,29,34],
            [16,16,22,24,27,29,34,37],
            [19,22,26,27,29,34,34,38],
            [22,22,26,27,29,34,37,40],
            [22,26,27,29,32,35,40,48],
            [26,27,29,32,35,40,48,58],
            [26,27,29,34,38,46,56,59],
            [27,29,35,38,46,56,69,83]])
    T = cv2.dct(g.astype(np.float32))
    QT = np.round(16.0*T/(Q*QF))
    IQT = np.round(QT*Q*QF/16)
    IT = np.round(cv2.idct(IQT))
    return IT.astype(np.uint8)

def image_dct_and_idct(I,QF):
    h,w = I.shape
    I = I[:8*int(h/8),:8*int(w/8)]
    output = np.zeros_like(I)
    for i in range(int(h/8)):
        for j in range(int(w/8)):
            output[i*8:(i+1)*8,j*8:(j+1)*8] = block_dct_and_idct(I[i*8:(i+1)*8,j*8:(j+1)*8],QF)
    return output


img = cv2.imread('./images/lena.jpg')
img_y = cv2.cvtColor(img,cv2.COLOR_RGB2YUV)[:,:,0] #get Y component
#QF = 1
img_QF1 = image_dct_and_idct(img_y,1) 
cv2.imshow("QF=1",img_QF1)
#QF = 20
img_QF20 = image_dct_and_idct(img_y,20)
cv2.imshow("QF=20",img_QF20)
#QF = 50
img_QF50 = image_dct_and_idct(img_y,50)
cv2.imshow("QF=50",img_QF50)
#QF = 100
img_QF100 = image_dct_and_idct(img_y,100)
cv2.imshow("QF=100",img_QF100)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
