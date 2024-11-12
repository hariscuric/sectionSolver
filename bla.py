import numpy as np


k=np.array([[1,2,3],[4,5,6],[7,8,9]])
ktt = k[[True,False,True],][:,[False,True,False]]

deltad = np.array([0,3,0])


a = np.matmul(ktt,deltad[[1]])

c = np.array([1])

d = np.zeros((3))

d[0:2] = a
d[2] = c[0]




deltad = np.array([4,3,0])




k1 = np.zeros((3,3))
k1[:] = k[:]
fpt = np.array([1,1])
fpc = np.array([2])
k1[0:2,2] = fpt
k1[2,2] = fpc[0]

print(k)
print(k1)
