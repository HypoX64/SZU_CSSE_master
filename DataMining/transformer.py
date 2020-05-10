import numpy as np
import random

def match_random(a,b):
    state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(state)
    np.random.shuffle(b)

def random_transform(a,alpha):
	return a*random.uniform(1-alpha,1+alpha)


def normlize(npdata,justprice = False):
    _min = np.min(npdata)
    _max = np.max(npdata)
    if justprice:       
        _min = 34900.0
        _max = 755000.0
    return (npdata-_min)/(_max-_min)


def convert2price(tensor):
    return tensor*(755000.0-34900.0)+34900

# def normlize(npdata,justprice = False):

#     return np.log1p(npdata)


# def convert2price(tensor):
#     return np.expm1(tensor)