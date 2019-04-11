import math
import matplotlib.pyplot as plt
import numpy as np

a=2
b=2.4


# s_list=[]
# v_list=[]
# x_list=[]
# y_list=[]
# yvals=[]
# for i in range(7000):
#     i=i/10000
#     v_list.append(i)
#     s=(-a*b*math.log(1-b/a*i)-b*i)/b**2
#     s_list.append(s)
#     yvals.append(3.712*i**3-2.561*i**2+2.778*i-1.041)
s_list=[3,4,5,6,7,8]
v_list=[1.2,1.3,1.5,2,2.6,3.5]
fig=plt.figure()
z1 = np.polyfit(s_list, v_list, 3)#用3次多项式拟合

p1 = np.poly1d(z1)

# z2 = np.polyfit(x_list, v_y_list, 3)#用3次多项式拟合
# p2 = np.poly1d(z2)
print(p1)
yvals=[]
x_list=[]
for i in range(2000,9000):
    i=i/1000
    x_list.append(i)
    # yvals.append(0.08*i**4-1.79*i**3+14.5*i**2-49.9*i+62.4)
    yvals.append(0.0037*i**3+0.039*i**2-0.32*i+1.738)
    # yvals.append(0.335*i**2-3.22*i+8.04)

# print(p2)
# yvals=p1(v_list)
plt.plot(s_list,v_list,color='black')
plt.plot(x_list,yvals,color='y')
plt.plot()
# plt.plot(x_list,sita_y_list,color='b')
plt.show()