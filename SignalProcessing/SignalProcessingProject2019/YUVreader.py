import cv2
import numpy as np
import os

def load(filename, width, height, startfrm=0, endfrm = None, type = 'YUV'):
    """
    :param filename: YUV video name
    :param height: YUV video height
    :param width: YUV video width
    :param startfrm: start frame
    :param endfrm: end frame
    :param type: output type 'YUV' 'BGR'
    :return: array like [frame,h,w,ch]
    """
    fp = open(filename, 'rb')

    framesize = height * width * 3 // 2  # 一帧图像所含的像素个数
    h_h = height // 2
    h_w = width // 2

    fp.seek(0, 2)  # 设置文件指针到文件流的尾部
    ps = fp.tell()  # 当前文件指针位置
    numfrm = ps // framesize  # 计算输出帧数
    fp.seek(framesize * startfrm, 0)

    if endfrm != None:
        numfrm = endfrm

    output = np.zeros(shape=(numfrm, height, width, 3), dtype='uint8', order='C')

    for i in range(numfrm - startfrm):
        Yt = np.zeros(shape=(height, width), dtype='uint8', order='C')
        Ut = np.zeros(shape=(h_h, h_w), dtype='uint8', order='C')
        Vt = np.zeros(shape=(h_h, h_w), dtype='uint8', order='C')

        for m in range(height):
            for n in range(width):
                Yt[m, n] = ord(fp.read(1))
        for m in range(h_h):
            for n in range(h_w):
                Ut[m, n] = ord(fp.read(1))
        for m in range(h_h):
            for n in range(h_w):
                Vt[m, n] = ord(fp.read(1))

        if type == 'YUV':
            output[i,:,:,0] = Yt
            output[i,:,:,1] = cv2.resize(Ut,(width,height ))
            output[i,:,:,2] = cv2.resize(Vt,(width, height))

        elif type == 'BGR':
            BGR = np.zeros(shape=(numfrm,height, width, 3), dtype='uint8', order='C')
            img = np.concatenate((Yt.reshape(-1), Ut.reshape(-1), Vt.reshape(-1)))
            img = img.reshape((height * 3 // 2, width)).astype('uint8')  # YUV 的存储格式为：NV12（YYYY UV）
            # 由于 opencv 不能直接读取 YUV 格式的文件, 所以要转换一下格式
            bgr_img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420)  # 注意 YUV 的存储格式
            output[i] = bgr_img
            if os.path.isdir('./yuv2bgr'):
                cv2.imwrite('yuv2bgr/%d.jpg' % (i + 1), bgr_img)
        
        # print("Extract frame %d " % (i + 1))

    fp.close()
    print('Read '+filename+' done!')
    return output


if __name__ == '__main__':
    _ = yuv2bgr(filename='dragon_video.yuv', width=640, height=480,startfrm=0)
