import numpy as np
from scipy import stats
import mesa as ms 
import matplotlib.pyplot as plt

def skewed_data(skew_parameter=-0.5, loc= 1.0, scale=1.0, size= 1):
    '''
    Create truncated skewed random variables
    agrs: 
        skew_parameter: float, skew parameter
        loc:            float, mean of the normal distribution
        scale:          float, standard deviation of the normal distribution
        size:           int, number of random variables
    '''

    data = stats.skewnorm.rvs(skew_parameter, loc=loc, scale=scale, size=size)
    data = np.round(data,2).astype(float) # Round to 2 decimals

    # Fixing Limitation for truncation
    for d_ix, d_value in enumerate(data):
        print(d_ix, d_value)
        if d_value < 0:
            print(d_ix, d_value, data[d_ix])
            data[d_ix] = 0
            print(d_ix, d_value, data[d_ix])
        elif d_value > 1:
            print(d_ix, d_value, data[d_ix])
            data[d_ix] = 1
            print(d_ix, d_value, data[d_ix])

    # Check if it worked
    
    assert data.any() < 0 or data.any() > 1, "Not All Data is between 0 and 1"

    return data


def truncated_normal_rvs(x_min = 0.0, x_max= 1.0, loc = 0.5, scale= 0.5/3, size = 3): 
    '''
    Create truncated normal random variables for preferences
    arg:
        x_min:  float, minimum value
        x_max:  float, maximum value
        loc:    float, mean of the normal distribution
        scale:  float, standard deviation of the normal distribution
        size:   int, number of random variables
    '''

    # Define upper and lower quantiles
    quantile1 = stats.norm.cdf(x_min, loc=loc, scale=scale)
    quantile2 = stats.norm.cdf(x_max, loc=loc, scale=scale)

    # return the truncated normal variable from the distribution
    return np.round(stats.norm.ppf(
        np.random.uniform(quantile1, quantile2, size=size),
        loc=loc,
        scale=scale),2).astype(float)