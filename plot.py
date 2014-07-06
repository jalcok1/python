import matplotlib.pyplot as plt
import numpy as np

N = 2000




x1 = np.linspace(0, 10, N, endpoint=True)
x2 = np.linspace(0, 10, N, endpoint=False)

y = np.zeros(N)
y2 = np.sin(2*np.pi*x1)
#*np.sin(np.pi*x1)
#plt.plot(x1, y, 'o')
#plt.plot(x2, y + 0.5, 'o')
plt.plot(x2, y2)
plt.ylim([-2, 2])
plt.legend(('sin()*sin()'))
plt.show()