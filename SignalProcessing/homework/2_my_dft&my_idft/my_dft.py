import numpy as np


def dft(Xn):
    '''
    @Hypo 1910273011
    This is a function for Discrete Fourier Transform(DFT)

    Parameters: 
    Xn : array_like, type = complex

    Returns:
    out : array_like, type = complex
    '''
    Xk = []; Xk_i = 0
    N = len(Xn)
    for k in range(N):
        for n in range(N):
            Xk_i += Xn[n]*np.exp(-1j*k*2*np.pi*n/N)
        Xk.append(Xk_i)
        Xk_i = 0
    return np.array(Xk)

def idft(Xk):
    '''
    @Hypo 1910273011
    This is a function for Inverse Discrete Fourier Transform(IDFT)

    Parameters: 
    Xn : array_like, type = complex

    Returns:
    out : array_like, type = complex
    '''

    # use dft calculate idft
    return dft(Xk.conjugate()).conjugate()/len(Xk)

    #use formula
    '''
    Xn = []; Xn_i = 0
    N = len(Xk)
    for n in range(N):
        for k in range(N):
            Xn_i += Xk[k]*np.exp(1j*k*2*np.pi*n/N)
        Xn.append(Xn_i)
        Xn_i = 0
    return np.array(Xn)/N
    '''