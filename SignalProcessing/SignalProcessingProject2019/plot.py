import numpy as np
import cv2
import time
from matplotlib import pyplot as plt

import YUVreader
import motion_compensation as mc

#load YUV
dragon_video = YUVreader.load('dragon_video.yuv', 640, 480, 0, 2,type='YUV')
gas_video = YUVreader.load('gas_video.yuv', 640, 480, 0,2,type='YUV')


#Find the right parameters
#Full Search
losss = []
windows = []
times = []
for window_size in range(3,30,1):
    t1 = time.time()
    pred = mc.full(dragon_video[1],dragon_video[0],window_size)
    t2 = time.time()
    times.append(t2-t1)
    losss.append(mc.rmse(pred,dragon_video[1]))
    windows.append(window_size)
plt.subplot(121)
plt.plot(windows,times)
plt.title('window size & cost time - Full Search')
plt.xlabel('window size')
plt.ylabel('cost time')
plt.subplot(122)
plt.plot(windows,losss)
plt.title('window size & rmse- Full Search')
plt.xlabel('window size')
plt.ylabel('rmse')
plt.show()
# predict_error = 0
# t1 = time.time

# plot image
dragon_video = YUVreader.load('dragon_video.yuv', 640, 480, 0, 2,type='BGR')
pred = mc.full(dragon_video[1],dragon_video[0],20)
img = np.zeros((480,640*3,3),dtype='uint8')
img[:,:640,:]=dragon_video[1]
img[:,640:640*2,:]=pred
img[:,640*2:,:]=np.abs(dragon_video[1]-pred)
cv2.namedWindow('image')
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()