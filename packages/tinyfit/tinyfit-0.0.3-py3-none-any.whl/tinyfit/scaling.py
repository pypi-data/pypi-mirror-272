# tinyfit/scaling.py

"""scaling provides feature scaling methods.

The module contains the following functions:

"""

import numpy as np
from typing import List

def minmax(x):
    """Scales the feature using min-max scaling.

        Args:
            x: The feature values to scale.

        Returns:
            array: The feature values scaled.
        """
    return (x - x.min(axis=0))/(x.max(axis=0) - x.min(axis=0))

def meannorm(x):
    """Scales the feature using mean normalisation.

        Args:
            x: The feature values to scale.

        Returns:
            array: The feature values scaled.
        """
    return (x - x.mean(axis=0))/(x.max(axis=0) - x.min(axis=0))

def zscore(x):
    """Scales the feature using z-score scaling.

        Args:
            x: The feature values to scale.

        Returns:
            array: The feature values scaled.
        """
    return (x - x.mean(axis=0))/x.std(axis=0)

class FeatureScaler():
    """A feature scaling class.

    A generic feature scaling class that can be used to scale multiple features in a dataset in one pass. 

    Attributes:
        scale_type: A list of strings indicating the type of scaling to be performed on each feature. "minmax" = `minmax().` "meannorm" = `meannorm()`. "zscore" = `zscore()`. The position of the string in the list must match the feature column position.
    """
    def __init__(self, scale_type: List[str] = ["meannorm"]):
        """Initializes the feature scaling class object.

        Args:
            scale_type: A list of strings indicating the type of scaling to be performed on each feature.
        """
        self.scale_type = scale_type

    def scale(self, data):
        """Returns the data scaled according to the scales types in scale_type.

        Args:
            data: The feature data to scale.

        Returns:
            array: The feature values scaled.
        """
        out = np.zeros(data.shape)

        for i in range(len(self.scale_type)):

            if self.scale_type[i] == 'minmax':
                out[:,i] = minmax(data[:,i])

            if self.scale_type[i] == 'meannorm':
                out[:,i] = meannorm(data[:,i])

            if self.scale_type[i] == 'zscore':
                out[:,i] = meannorm(data[:,i])

        return out