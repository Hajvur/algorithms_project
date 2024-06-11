
from numpy import random


def monte_carlo(attraction_list,n):
    new_list = []
    new_list.append(attraction_list[0]) 
    copy_ver = attraction_list[1:].shuffle()
    for i in range(n-1):
        new_list.append(copy_ver[i])
    
    return new_list




        