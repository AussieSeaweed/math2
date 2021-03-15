from random import shuffle

import numpy as np
from auxiliary import trimmed


def trimmed_mean(values, percentage):
    """Calculates the trimmed mean of the values.

    :param values: The values.
    :param percentage: The trimmed percentage.
    :return: The trimmed mean.
    """
    return np.mean(np.fromiter(trimmed(sorted(values), percentage), float))


def range_(values):
    """Calculates the range of the values.

    :param values: The values.
    :return: The range of the values.
    """
    array = np.fromiter(values, float)

    return np.max(array) - np.min(array)


def shuffled(values):
    """Shuffles the copied values and returns the list.

    :param values: The values to be shuffled.
    :return: The shuffled sequence.
    """
    values = list(values)

    shuffle(values)

    return values
