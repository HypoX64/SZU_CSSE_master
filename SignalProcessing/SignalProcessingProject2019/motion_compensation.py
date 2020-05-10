import numpy as np

def mse(predictions, targets):
    return np.mean((predictions-targets)**2)

def rmse(predictions, targets):
    return np.sqrt(mse(predictions, targets))

def psnr(predictions, targets):
    return 10*np.log10((255*255)/mse(predictions, targets))

############################################################################
# full search
############################################################################
def full(fr,fr_ref,search_win):
    """
    :param fr: the frame need to predict
    :param fr_ref: previous frame
    :param search_win: full search window size
    :return fr_out: predict frame
    """
    height,width = fr.shape[:2]
    fr_out = np.zeros_like(fr,dtype='uint8')
    for i in range(0,height,16):
        for j in range(0,width,16):
            loss = 1e10
            ref_h = i
            ref_w = j
            blk = fr[i:i+16,j:j+16]
            for y in range(i-search_win,i+search_win):
                for x in range(j-search_win,j+search_win):
                    if x>0 and y>0 and x<width-16 and y<height-16:
                        ref_blk = fr_ref[y:y+16,x:x+16]
                        loss_this = rmse(ref_blk,blk)
                        if loss_this < loss:
                            loss = loss_this
                            ref_h = y
                            ref_w = x
            fr_out[i:i+16,j:j+16] = fr_ref[ref_h:ref_h+16,ref_w:ref_w+16]
    return fr_out

############################################################################
# Three-step search
############################################################################
def get_multi_step_point(h,w,stride):
    h = h - stride
    w = w - stride 
    points = []
    for i in range(3):
        for j in range(3):
            points.append([h+i*stride,w+j*stride])
    return points

def multi_step_substep(ref_h,ref_w,loss,fr_ref,blk,stride):
    height,width = fr_ref.shape[:2]
    points = get_multi_step_point(ref_h,ref_w,stride)
    for point in points:
        h,w = point
        if h>0 and w>0 and w<width-16 and h<height-16:
            ref_blk = fr_ref[h:h+16,w:w+16]
            loss_this = rmse(ref_blk,blk)
            if loss_this < loss:
                loss = loss_this
                ref_h = h
                ref_w = w
    return loss,ref_h,ref_w

def multi_step(fr,fr_ref,step_num):
    """
    :param fr: the frame need to predict
    :param fr_ref: previous frame
    :param step_num: step number if 3 -> Three-step search
    :return fr_out: predict frame
    """
    height,width = fr.shape[:2]
    fr_out = np.zeros_like(fr,dtype='uint8')
    for h in range(0,height,16):
        for w in range(0,width,16):
            loss = 1e10
            ref_h = h
            ref_w = w
            blk = fr[h:h+16,w:w+16]
            for step_cnt in range(step_num):
                loss,ref_h,ref_w = multi_step_substep(ref_h,ref_w,loss,fr_ref,blk,int(2**(step_num-step_cnt-1)))
            fr_out[h:h+16,w:w+16] = fr_ref[ref_h:ref_h+16,ref_w:ref_w+16]
    return fr_out

############################################################################
# Diamond search
############################################################################
def get_diamond_point(h,w,wide,stride = 1):

    points = []
    if wide == 2:
        points = [[h,w],[h+1,w],[h-1,w],[h,w+1],[h,w-1]]
    elif wide ==3:
        points = [[h,w],[h+2*stride,w],[h-2*stride,w],[h,w+2*stride],[h,w-2*stride],[h+stride,w+stride],[h-stride,w-stride],[h+stride,w-stride],[h-stride,w+stride]]
    return points

def multi_diamond_substep(ref_h,ref_w,loss,used_points,fr_ref,blk,wide):
    height,width = fr_ref.shape[:2]
    points = get_diamond_point(ref_h,ref_w,wide)
    for point in points:
        if point not in used_points: 
            used_points.append(point)
            h,w = point
            if h>0 and w>0 and w<width-16 and h<height-16:
                ref_blk = fr_ref[h:h+16,w:w+16]
                loss_this = rmse(ref_blk,blk)
                if loss_this < loss:
                    loss = loss_this
                    ref_h = h
                    ref_w = w
    return ref_h,ref_w,loss,used_points

def diamond(fr,fr_ref):
    """
    :param fr: the frame need to predict
    :param fr_ref: previous frame
    :return fr_out: predict frame
    """
    height,width = fr.shape[:2]
    fr_out = np.zeros_like(fr,dtype='uint8')
    for h in range(0,height,16):
        for w in range(0,width,16):
            
            loss = 1e10
            ref_h = h
            ref_w = w
            blk = fr[h:h+16,w:w+16]
            used_points = []

            #step1 LDSP
            cnt = 0
            while(1):
                cnt += 1
                input_h = ref_h
                input_w = ref_w
                ref_h,ref_w,loss,used_points = multi_diamond_substep(ref_h,ref_w,loss,used_points,fr_ref,blk,3)
                if (input_h == ref_h) and (input_w == ref_w):
                    break

            #step2 SDSP
            ref_h,ref_w,loss,_ = multi_diamond_substep(ref_h,ref_w,loss,used_points,fr_ref,blk,2)

            fr_out[h:h+16,w:w+16] = fr_ref[ref_h:ref_h+16,ref_w:ref_w+16]
    return fr_out


def main():

    print(get_diamond_point(128,128,3))

if __name__ == "__main__":
    main()