import numpy as np
import cv2
import time
from matplotlib import pyplot as plt

import YUVreader
import motion_compensation as mc

#load YUV
dragon_video = YUVreader.load('dragon_video.yuv', 640, 480, 0, type='YUV')
gas_video = YUVreader.load('gas_video.yuv', 640, 480, 0,type='YUV')


def core(mc_mod,video):
    rmse_error = 0
    psnr_error = 0
    t1 = time.time()
    for i in range(len(video)-1):
        ref_frame = video[i]
        curr_frame = video[i+1]

        if mc_mod == 'full':
            curr_frame_predicted = mc.full(curr_frame, ref_frame,5)
        elif mc_mod == 'three_step':
            curr_frame_predicted = mc.multi_step(curr_frame, ref_frame,3)
        elif mc_mod == 'multi_step':
            curr_frame_predicted = mc.multi_step(curr_frame, ref_frame,4)
        elif mc_mod == 'diamond':
            curr_frame_predicted = mc.diamond(curr_frame, ref_frame)

        rmse_error = rmse_error + mc.rmse(curr_frame_predicted, curr_frame)
        psnr_error = psnr_error + mc.psnr(curr_frame_predicted, curr_frame)
    t2 = time.time()
    return rmse_error/(len(video)-1), psnr_error/(len(video)-1),t2-t1

#Full Search
print('-------Full Search-------')
#dragon_video
_rmse,_psnr,_time = core('full',dragon_video)
print('dragon_video  rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))
#gas_video
_rmse,_psnr,_time = core('full',gas_video)
print('gas_video     rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))


#Three-step search
print('-------Three-step search-------')
#dragon_video
_rmse,_psnr,_time = core('three_step',dragon_video)
print('dragon_video  rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))
#gas_video
_rmse,_psnr,_time = core('three_step',gas_video)
print('gas_video     rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))

#Multi-Step search
print('-------Multi-Step search-------')
#dragon_video
_rmse,_psnr,_time = core('multi_step',dragon_video)
print('dragon_video  rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))
#gas_video
_rmse,_psnr,_time = core('multi_step',gas_video)
print('gas_video     rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))

#Diamond Search
print('-------Diamond Search-------')
#dragon_video
_rmse,_psnr,_time = core('diamond',dragon_video)
print('dragon_video  rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))
#gas_video
_rmse,_psnr,_time = core('diamond',gas_video)
print('gas_video     rmse:{:.3f}  psnr:{:.3f}  time:{:.3f}'.format(_rmse,_psnr,_time))