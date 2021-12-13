import matplotlib.pyplot as plt
import numpy as np


# x = np.arange(0, 4*np.pi, 0.1)
# y = np.sin(x)

# x = np.arange(-4*np.pi, 4*np.pi, 0.1)
# y = np.cbrt(x)

# x = np.arange(0, 4*np.pi, 0.1)
# y = np.log(x) * -1

# x = np.arange(-5*np.pi, 5*np.pi, 0.1)
# y = x ** 2

x = np.arange(-5*np.pi, 5*np.pi, 0.1)
y = (1/x)*np.sin(x)*50


print(y)
plt.scatter(x, y)
plt.show()
