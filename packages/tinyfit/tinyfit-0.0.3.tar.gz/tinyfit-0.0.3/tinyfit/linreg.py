# tinyfit/linreg.py

"""linreg provides linear regression methods.

The module contains the following functions:

"""

import numpy as np
from typing import Optional

class LinearRegression():
    """Linear regression model.

    A generic linear regression model class to be used for simple (single) or multiple regression 
    of the for y = W*X + b where W*X is the dot product between the feature weights and the 
    input data and b is the bias. 

    Attributes:
        n_features: The number of features to fit.
        bias: Includes a bias term to the model.
        lr: The learning rate of the model.
        W: The weights matrix.
        b: The model bias.
    """
    def __init__(self, n_features: Optional[int] = 1, bias: Optional[bool] = True, lr: Optional[float] = 0.01):
        """Initializes the linear regression class object.

        Args:
            n_features: Sets the number of features to be fit.
            bias: Whether or not to include a bias term to the model.
            lr: Sets the learning rate of the model.
        """
        self.n_features = n_features
        self.bias = bias
        self.W = np.ones((n_features,1))
        self.b = np.zeros((1,1))
        self.lr = lr

    def details(self):
        """Prints the details of the model"""
        print(f'''Model contains {self.n_features} features (bias={self.bias}) \nweights: {self.W} \nbias= {self.b}''')

    def fit(self, x, y, iter: Optional[int] = 1):
        """Fits the model to the provided data using mean squared error and gradient descent.

        Args:
            x: The data feature values.
            y: The data target values.
            iter: The amount of steps for gradient descent.
        """

        for i in range(iter):
            x = x.reshape(-1,self.n_features)
            y = y.reshape(-1,1)
            pred = x.dot(self.W) + self.b
            diff = pred - y
            square = diff.T.dot(diff)
            mse = square/x.shape[0]
            
            grad_W = x.T.dot(diff)/x.shape[0]
            self.W += -self.lr*grad_W
            if self.bias:
                grad_b = 2*np.sum(diff,keepdims=True)/x.shape[0]
                self.b += - self.lr*grad_b
                
        print(f'mse= {mse.item():.4f}')

    def predict(self, x):
        """Predicts the value y for the given feature(s).

        Args:
            x: The feature values to pass through the model.

        Returns:
            array: Predicted y values.
        """
        x = x.reshape(-1,self.n_features)
        return x.dot(self.W) + self.b

    def calculate_mse(self, x, y):
        """Calculates the mean squared error for the model according to a given set of feature and target values.

        Args:
            x: The data feature values.
            y: The data target values.

        Returns:
            float: Mean squared error.
        """
        x = x.reshape(-1,self.n_features)
        y = y.reshape(-1,1)
        pred = x.dot(self.W) + self.b
        diff = pred - y
        square = diff.T.dot(diff)
        mse = square/x.shape[0]
        return mse