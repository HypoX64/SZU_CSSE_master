predict_error = 0
timer_start
for i = 0 to num_frames-2
ref_frame = read_frame(i)
curr_frame = read_frame(i+1)
curr_frame_predicted = motion_estimation (ref_frame, curr_frame)
predict_error = predict_error + rmse(curr_frame, curr_frame_predicted)
endfor
time_used = timer_stop
avg_prediction_error = prediction_error/(num_frames-1)

0.6895990682998346  cost time: 0.152 s


# dragon_video = YUVreader.yuv2bgr('dragon_video.yuv', 640, 480, 0, 2,type='YUV')
# t1 = time.time()
# fr_out,loss = mc.full(dragon_video[1],dragon_video[0],4)
# t2 = time.time()
# print(loss,' cost time:','%.3f'%(t2-t1),'s')


dragon_video = YUVreader.yuv2bgr('dragon_video.yuv', 640, 480, 0, 2,type='YUV')
t1 = time.time()

fr_out,loss = mc.multi_step(dragon_video[1],dragon_video[0],5)
t2 = time.time()
print(loss,' cost time:','%.3f'%(t2-t1),'s')


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',fr_out[:,:,0])
cv2.waitKey(0)
cv2.destroyAllWindows()