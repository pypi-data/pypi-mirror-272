import src.tinyfit.linreg as lr
import numpy as np

#lreg = lr.LinearRegression(n_features=2, bias=True)
#X, y = np.array([[1,1.5],[2,2.5],[3,3.5],[4,4.5],[5,5.5]]), np.array([3,4,5,6,7])

lreg = lr.LinearRegression(n_features=1, bias=True)
X, y = np.array([1,2,3,4,5]), np.array([3,4,5,6,7])

lreg.fit(X,y, iter=100)
