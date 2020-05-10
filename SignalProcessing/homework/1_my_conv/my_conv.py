import numpy as np


def conv(u,v):
    '''
    @Hypo 1910273011
    This is a function to conv two vectors

    Parameters: 
    u : array_like
    v : array_like

    Returns:
    out : array_like
    '''
    out_length = len(u)+len(v)-1
    w_length = 2*(len(u)-1)+len(v)
    out = np.zeros(out_length)
    u_flip = u[::-1] #flip u

    v_pad = np.zeros(w_length)
    v_pad[len(u)-1:len(u)+len(v)-1] = v # fill 0 to v

    #shift, multiple, sum
    for i in range(out_length):
        out[i] = np.sum(u_flip*v_pad[i:i+len(u)])

    return out
