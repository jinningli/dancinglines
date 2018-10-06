# ===================================================== #
# Implementation of wDTW-CD python module               #
# ===================================================== #

from numpy import array, zeros, argmin, inf, e


def wdtwcd(choice, x, y, dist):
    # """
    # Aligns two sequences by weighted Dynamic Time Warping with compound distance (wDTW-CD).
    #
    # :param array x: N1*M array
    # :param array y: N2*M array
    # :param func dist: distance used as cost measure
    #
    # Returns the classic DTW distance, the cost matrix, the accumulated cost matrix, the warping path (alignment path), the derivative sequences of x and y.
    # """
    assert len(x)
    assert len(y)
    r, c = len(x), len(y)
    xd = x.copy()
    yd = y.copy()
    for i in range(r):
        if (i == 0):
            xd[i] = 0
        elif (i == r - 1):
            xd[i] = (x[i] - x[i - 1]) / 2
        else:
            xd[i] = (x[i] - x[i - 1] + (x[i + 1] - x[i - 1]) / 2) / 2
    for i in range(c):
        if (i == 0):
            yd[i] = 0
        elif (i == c - 1):
            yd[i] = (y[i] - y[i - 1]) / 2
        else:
            yd[i] = (y[i] - y[i - 1] + (y[i + 1] - y[i - 1]) / 2) / 2
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            if choice <= 2:
                D1[i, j] = dist(x[i], y[j])  # dist
            elif choice <= 4:
                D1[i, j] = dist(xd[i], yd[j])  # derivative
            elif choice == 5:
                D1[i, j] = dist(x[i], y[j]) + 1 / (1 + e ** (10.0 * (3 - abs(i - j))))  # dist + logistic
            elif choice == 6:
                D1[i, j] = dist(xd[i], yd[j]) + 1 / (1 + e ** (10.0 * (3 - abs(i - j))))  # derivative + logistic
            elif choice == 7:
                D1[i, j] = ( (dist(xd[i], yd[j]))  * dist(x[i], y[j]) ) ** 0.5 + 1 / (
                    1 + e ** (10.0 * (3 - abs(i - j))))  # derivative + dist + logistic1
            elif choice == 8:
                D1[i, j] = ( (dist(xd[i], yd[j]))  * dist(x[i], y[j]) ) ** 0.5 + 1 / (
                    1 + e ** (5.0 * (3.2 - abs(i - j))))  # derivative + dist + logistic2
            elif choice == 9:
                D1[i, j] = ( (dist(xd[i], yd[j]))  * dist(x[i], y[j]) ) ** 0.5 + 1 / (
                    1 + e ** (5.0 * (2.2 - abs(i - j))))  # derivative + dist + logistic3
            else:
                D1[i, j] = ( (dist(xd[i], yd[j])) * dist(x[i], y[j]) ) ** 0.5 # dist + deravative
    C = D1.copy()
    for i in range(r):
        for j in range(c):
            if ((choice == 2) or (choice == 4)):
                D1[i, j] += min(D0[i, j], 1.2 * D0[i, j + 1], 1.2 * D0[i + 1, j])  # factor
            else:
                D1[i, j] += min(D0[i, j], D0[i, j + 1], D0[i + 1, j])  # non-factor
    if len(x) == 1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path, xd, yd


def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while ((i > 0) or (j > 0)):
        tb = argmin((D[i, j], D[i, j + 1], D[i + 1, j]))
        if (tb == 0):
            i -= 1
            j -= 1
        elif (tb == 1):
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)