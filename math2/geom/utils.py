from math2.linalg import row


def distance(p1, p2):
    return abs(row(p1) - row(p2))