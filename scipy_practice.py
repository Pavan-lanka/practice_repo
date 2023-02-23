import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
x = np.random.randint(10,100,50)
y = np.random.randint(2010,2015,50)

slope, intercept, r, p, std_err = sp.stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()

