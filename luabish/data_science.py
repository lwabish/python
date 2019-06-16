from datetime import date
from scipy.optimize import newton, brentq


def xnpv(rate, values, dates):
    '''Equivalent of Excel's XNPV function.

    >>> from datetime import date
    >>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
    >>> values = [-10000, 20, 10100]
    >>> xnpv(0.1, values, dates)
    -966.4345...
    '''
    if rate <= -1.0:
        return float('inf')
    d0 = dates[0]    # or min(dates)
    return sum([vi / (1.0 + rate)**((di - d0).days / 365.0) for vi, di in zip(values, dates)])


def xirr_scipy(values, dates):
    '''Equivalent of Excel's XIRR function.

    >>> from datetime import date
    >>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
    >>> values = [-10000, 20, 10100]
    >>> xirr(values, dates)
    0.0100612...
    '''
    try:
        return newton(lambda r: xnpv(r, values, dates), 0.0)
    except RuntimeError:    # Failed to converge?
        return brentq(lambda r: xnpv(r, values, dates), -1.0, 1e10)


def xirr(transactions):
    years = [(ta[0] - transactions[0][0]).days / 365.0 for ta in transactions]
    residual = 1
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = 0.0
        for i, ta in enumerate(transactions):
            residual += ta[1] / pow(guess, years[i])
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0
    return guess-1


if __name__ == '__main__':
    tas = [(date(2010, 12, 29), -10000),
           (date(2012, 1, 25), 20),
           (date(2012, 3, 8), 10100.01)]
    print(xirr(tas))  # 0.0100612640381
    print(xirr_scipy([-10000, 20, 10100],
                     [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]))
