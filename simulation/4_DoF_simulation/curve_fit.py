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
v_list=[2.79,2.91,2.97,3.05,3.14]
s_list=[-1.1,-1.05,-1,-0.75,0]
fig=plt.figure()
z1 = np.polyfit(v_list, s_list, 1)#用3次多项式拟合

p1 = np.poly1d(z1)

# z2 = np.polyfit(x_list, v_y_list, 3)#用3次多项式拟合
# p2 = np.poly1d(z2)
print(p1)
yvals=[]
x_list=[]
for i in range(279,317):
    i=i/100
    x_list.append(i)
    # yvals.append(0.08*i**4-1.79*i**3+14.5*i**2-49.9*i+62.4)
    yvals.append(57.88*i**3-500*i**2+1440*i-1383.7)
    # yvals.append(0.335*i**2-3.22*i+8.04)

# print(p2)
# yvals=p1(v_list)
plt.plot(v_list,s_list,color='black')
plt.plot(x_list,yvals,color='y')
plt.plot()
# plt.plot(x_list,sita_y_list,color='b')
plt.show()