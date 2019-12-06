import numpy as np
import random

def match_random(a,b):
    state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(state)
    np.random.shuffle(b)

def random_transform(a,alpha):
	return a*random.uniform(1-alpha,1+alpha)