# -*- coding: utf-8 -*-


def z_binomial_superiority_test(v1, v2, delta=0.):
    """
    Perform Test for Non-Inferiority/Superiority for Binomial samples.
    Returns test statistic and p-value.
    
    Method provided by Chow, Sample Size Calculations in Clinical Research (2nd ed., 2008), 4.2.2.
    
    p1 is the true mean of the first variation, p2 is the true mean of the second variation. epsilon = p1 - p2.
    Null hypothesis H0: epsilon <= delta.
    Alternative hypothesis H1: epsilon > delta.
    
    :param Variation v1: 
    :param Variation v2: 
    :param float delta: superiority margin
    :return tuple: 
    """
    from scipy.stats import norm
    from numpy import sqrt
    p1_hat = v1.estimate_conversion()
    p2_hat = v2.estimate_conversion()
    n1 = v1.total
    n2 = v2.total
    pe = p1_hat - p2_hat - delta  # point estimation
    var = p1_hat * (1 - p1_hat) / n1 + p2_hat * (1 - p2_hat) / n2  # variance estimation
    z = pe / sqrt(var)  # test statistic
    p_value = norm.sf(z)  # p-value
    return z, p_value
