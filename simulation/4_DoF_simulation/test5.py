import math
import numpy as np
from pid2 import PID
for i in range (0,30):
    print(i)
x_e=np.hstack((np.linspace(-1,1,30),np.linspace(1,-1,30)))
print(x_e)