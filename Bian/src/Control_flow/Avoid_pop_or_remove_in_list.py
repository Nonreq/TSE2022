x = ['a', 'b', 'c', 'd']
y = ['b', 'c']
x_new = []
for i in x:
    if i not in y:
       #x.pop()
       x_new.append(i)
x = x_new
print (x)
