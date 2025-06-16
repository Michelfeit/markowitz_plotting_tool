import math
import random
from random import Random

import numpy as np
import matplotlib.pyplot as plt
from values import mean, sigma, cov

def gen_random_pf_alloc(n:int, cap:bool):
    """
    for a given amount of assets, generates a random portfolio allocation. Optionally, the percentages cna be capped so
    so that not one asset dominates the rest of the assets.
    :param n: number of assets
    :param cap: whether to cap the allocation or not
    :return: allocation vector, sums up to 1
    """
    cumulative = 0
    allocation = np.zeros(n)
    for i in range(0,n-1):
        upper_limit = 1-cumulative
        if cap: upper_limit = min(2/n, upper_limit)
        x = random.uniform(0,upper_limit)
        allocation[i] = x
        cumulative += x
        print(x)
    allocation[n-1] = 1 - cumulative
    assert(np.sum(allocation) == 1)
    return allocation

def calc_allocation_return_and_risk(allocation:np.array):
    pass
t = gen_random_pf_alloc(5, True)

print(t)
print(np.sum(t))
