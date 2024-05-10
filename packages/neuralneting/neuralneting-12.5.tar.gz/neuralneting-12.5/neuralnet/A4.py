def a4():
    print('''

import numpy as np
import matplotlib.pyplot as plt

#bipolar
X = np.array([[-1, -1], [1, -1], [-1, 1], [1, 1]])
Y = np.array([-1, -1, -1, 1])

w = np.zeros(X.shape[1])
b = 0
alpha=0.3

for _ in range(20):
    for i in range(X.shape[0]):
        y_pred = np.sign(np.dot(X[i], w) + b)

        if y_pred != Y[i]:
            w += alpha * Y[i] * X[i]
            b += alpha * Y[i]

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
plt.scatter(X[:, 0], X[:, 1])

slope = -w[0] / w[1]
intercept = -b / w[1]
plt.plot([x_min, x_max], [x_min * slope + intercept, x_max * slope + intercept])

plt.xlabel('X1')
plt.ylabel('X2')
plt.title('Perceptron Decision Region')
plt.show()''')
a4()