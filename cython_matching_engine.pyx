# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

cimport cython

cpdef double best_buy_price(list prices):
    cdef Py_ssize_t i
    cdef double best

    if len(prices) == 0:
        return 0.0

    best = prices[0]

    for i in range(1, len(prices)):
        if prices[i] > best:
            best = prices[i]

    return best


cpdef double best_sell_price(list prices):
    cdef Py_ssize_t i
    cdef double best

    if len(prices) == 0:
        return 0.0

    best = prices[0]

    for i in range(1, len(prices)):
        if prices[i] < best:
            best = prices[i]

    return best