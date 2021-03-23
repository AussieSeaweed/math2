def series_sum(*args):
    """Calculates the series sum of the interval.

    :param args: stop or start, stop[, n]
    :return: the series sum.
    """
    if not args or len(args) > 3:
        raise ValueError('Invalid number of arguments')
    elif len(args) == 1:
        return series_sum(0, args[0])
    elif len(args) == 2:
        return series_sum(args[0], args[1], abs(args[1] - args[0]) + 1)
    else:
        start, stop, n = args

        return (start + stop) * n // 2


def frange(*args):
    if not args or len(args) > 3:
        raise ValueError('Invalid number of arguments')
    elif len(args) == 1:
        yield from frange(0, args[0])
    elif len(args) == 2:
        yield from frange(args[0], args[1], 1)
    else:
        start, stop, step = args

        while start < stop:
            yield start
            start += step
