from tensorflow.math import reduce_mean, reduce_std
from tensorflow import multiply


def correlation(x, y):
    """correlation function between two values

    Args:
        x (Tensor): set of given values
        y (Tensor): set of expected values

    Returns:
        Float: the value of correlation between x and y
    """    
    mx = reduce_mean(x)
    my = reduce_mean(y)
    xm, ym = x-mx, y-my
    r_num = reduce_mean(multiply(xm, ym))
    r_den = reduce_std(xm) * reduce_std(ym)
    return r_num / r_den
