def Logistic(x,u,i):
    for i in range(0,i):
        x=u*x*(1-x)
        print('result',x,i)

Logistic(0.1,4,10)


