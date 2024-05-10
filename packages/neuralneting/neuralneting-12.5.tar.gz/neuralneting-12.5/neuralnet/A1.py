def a1():
	print('''

import numpy as np
import math
from matplotlib import pyplot as plt

x=np.linspace(-5,5,100);

plt.plot(x,1/(1+np.exp(-x)),label="sigmoid")
plt.plot(x,np.maximum(0,x),label="ReLU")

tanhy=[]
for i in x:
	tanhy.append((math.exp(i)-math.exp(-i))/(math.exp(i)+math.exp(-i)))
plt.plot(x,tanhy,label="tanh");

plt.plot(x,x,label="identity")
plt.plot(x,np.exp(x)/np.sum(np.exp(x)),label="Softmax")




plt.legend()
plt.plot()
plt.show()
''')
a1()