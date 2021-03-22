def series_sum(*args):
    """Calculates the series sum of the interval.

    :param args: stop or start[, stop[, n]]
    :return: the series sum.
    """
    if not args:
        raise ValueError('Not enough arguments')
    if len(args) == 1:
        return series_sum(0, args[0])
    elif len(args) == 2:
        return series_sum(args[0], args[1], abs(args[1] - args[0]) + 1)
    else:
        start, stop, n = args

        return (start + stop) * n // 2
