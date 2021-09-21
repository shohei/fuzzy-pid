from control.matlab import *
import matplotlib.pyplot as plt
import pdb

s = tf('s')
G = 1/(1+s)
y,t = step(G)

plt.plot(t,y)
plt.show()