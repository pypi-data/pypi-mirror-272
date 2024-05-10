import numpy as np

def minmax(x):
    return (x - x.min(axis=0))/(x.max(axis=0) - x.min(axis=0))

def meannorm(x):
    return (x - x.mean(axis=0))/(x.max(axis=0) - x.min(axis=0))

def zscore(x):
    return (x - x.mean(axis=0))/x.std(axis=0)

class FeatureScaler():
    def __init__(self, scale_type = []):
        self.scale_type = scale_type

    def scale(self, data):
        '''
        Returns the data scaled according to the scales types in scale_type.
        '''
        out = np.zeros(data.shape)

        for i in range(len(self.scale_type)):

            if self.scale_type[i] == 'minmax':
                out[:,i] = minmax(data[:,i])

            if self.scale_type[i] == 'meannorm':
                out[:,i] = meannorm(data[:,i])

            if self.scale_type[i] == 'zscore':
                out[:,i] = meannorm(data[:,i])

        return out