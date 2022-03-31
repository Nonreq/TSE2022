# coding:utf-8
import math

def CPM(u,p,m,x):
    if  0 <= x <p:
        divmod((math.cos(m * math.cos(u * math.acos(x)))+x/p), 1)
    elif p <= x < 0.5:
        divmod(math.sin(math.cos(u*math.acos(x))) + (x-p)/(0.5-p), 1)
    else:
        CPM(u,p,1-x)
    return x

# print(CPM(2,0.8,0.5,0.4))
