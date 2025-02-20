import math as m


D1 = 17
D2 = 10

T1=1.44
T2=1.5
ksi1=0.05
ksi2=0.05

A=8*m.sqrt(ksi1*ksi2)*(ksi2+ksi1*T2/T1)*(T2/T1)**1.5
B=(1-(T2/T1)**2)**2
C=4*ksi1*ksi2*(1+(T2/T1)**2)*(T2/T1)
D=4*(ksi1**2+ksi2**2)*(T2/T1)**2

ro=A/(B+C+D)

Gap = m.sqrt(D1**2+D2**2-2*ro*D1*D2)


print(Gap)