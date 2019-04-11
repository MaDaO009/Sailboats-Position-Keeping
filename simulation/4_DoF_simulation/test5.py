import math
from pid2 import PID
a=PID()
[c,
d]=[1,
2]
print(a.update(1,0))
print(c,d)