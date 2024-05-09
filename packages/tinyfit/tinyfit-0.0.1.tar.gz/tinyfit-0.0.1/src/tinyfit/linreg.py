import numpy as np

class LinearRegression():
    def __init__(self, n_features= 1, bias= True, lr=0.01):
        self.n_features = n_features
        self.bias = bias
        self.W = np.ones((n_features,1))
        self.b = np.zeros((1,1))
        self.lr = lr

    def details(self):
        print(f'''Model contains {self.n_features} features (bias={self.bias}) \nweights: {self.W} \nbias= {self.b}''')

    def fit(self, x, y, iter=1):

        for i in range(iter):
            x = x.reshape(-1,self.n_features)
            y = y.reshape(-1,1)
            pred = x.dot(self.W) + self.b
            diff = pred - y
            square = diff.T.dot(diff)
            mse = square/self.n_features
            
            grad_W = x.T.dot(diff)/self.n_features
            self.W += - self.lr*grad_W
            if self.bias:
                grad_b = 2*np.sum(diff,keepdims=True)/self.n_features
                self.b += - self.lr*grad_b
                
        print(f'{mse=}')

    def calculate_mse(self, x, y):
        x = x.reshape(-1,self.n_features)
        y = y.reshape(-1,1)
        pred = x.dot(self.W) + self.b
        diff = pred - y
        square = diff.T.dot(diff)
        mse = square/self.n_features
        return mse