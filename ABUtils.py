# -*- coding: utf-8 -*-


def z_binomial_superiority_test(v1, v2, delta=0.):
    """
    Perform Test for Non-Inferiority/Superiority for Binomial samples.
    Returns test statistic and p-value.
    
    Method provided by Chow, Sample Size Calculations in Clinical Research (2nd ed., 2008), 4.2.2.
    
    p1 is the true mean of the first variation, p2 is the true mean of the second variation. 
    epsilon = p1 - p2.
    Null hypothesis H0: epsilon <= delta.
    Alternative hypothesis H1: epsilon > delta.
    
    :param Variation v1: first variation
    :param Variation v2: second variation
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


def z_binomial_test(v1, v2):
    """
    Perform Test for comparison of binomial samples' means.
    Returns test statistic and p-value.
    
    Method provided by Kobzar AI, Applied Mathematical Statistics for Engineers and Scientists (2006), 4.1.3.1
    (Кобзарь А. И. Прикладная математческая статистика для инженеров и научных работников (2006), 4.1.3.1)
    
    p1 is the true mean of the first variation, p2 is the true mean of the second variation.
    Null hypothesis H0: p1 = p2.
    Alternative hypothesis H1: p1 > p2.
    
    :param Variation v1: first variation
    :param Variation v2: second variation
    :return tuple:
    """
    from scipy.stats import norm
    from numpy import sqrt

    m1 = v1.success
    m2 = v2.success
    n1 = v1.total
    n2 = v2.total
    pe = m1 / n1 - m2 / n2 + 0.5 * (1 / n1 - 1 / n2)  # point estimation
    var = ((m1 + m2) / (n1 + n2) *
           (n1 + n2 - m1 - m2) / (n1 + n2) *
           (1 / n1 + 1 / n2)
           )  # variance estimation
    z = pe / sqrt(var)  # test statistic
    p_value = norm.sf(z)  # p-value

    return z, p_value


def f_binomial_test(v1, v2):
    """
    Perform Fisher's Exact test of binomial samples' means.
    Returns test statistic and p-value.
    
    Method provided by G. Casella, L. Berger, Statistical Inference (2-nd ed., 2002), Example 8.3.30
    
    p1 is the true mean of the first variation, p2 is the true mean of the second variation.
    Null hypothesis H0: p1 = p2.
    Alternative hypothesis H1: p1 > p2.
    
    :param Variation v1: first variation
    :param Variation v2: second variation
    :return tuple:
    """
    from numpy import array
    from scipy.stats import fisher_exact

    table = array([[v1.success, v2.success],
                   [v1.total - v1.success, v2.total - v2.success]
                   ])  # 2x2 contingency table
    return fisher_exact(table, 'greater')


if __name__ == '__main__':
    import ABTypes

    var1 = list(map(int, input('Введите total и success первой вариации: ').split()))
    var1 = ABTypes.Variation(*var1)

    var2 = list(map(int, input('Введите total и success второй вариации: ').split()))
    var2 = ABTypes.Variation(*var2)

    tests = [z_binomial_superiority_test, z_binomial_test, f_binomial_test]
    for test in tests:
        print(test)
        print(test(var1, var2))
        print(test(var2, var1))
        print('-' * 80)
