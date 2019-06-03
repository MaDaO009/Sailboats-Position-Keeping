import numpy as np 
a=np.array([[1,3],[2,4]])
a[0].append(1)
print(a[0])

a[0]=np.append(a[0],1)
