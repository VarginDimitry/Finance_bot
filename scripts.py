from datetime import datetime
import random


def dateTest():
    month_ago = datetime.now()
    print(month_ago)
    month_ago = month_ago.replace(microsecond=0, month=month_ago.month - 1)
    print(month_ago)


def QuickSort(a: list):
    if len(a) <= 1:
        return a
    left = [x for x in a[1:] if x <= a[0]]
    rigth = [x for x in a[1:] if x > a[0]]
    return QuickSort(left) + [a[0]] + QuickSort(rigth)


def isCool(a: list):
    if len(a) == 2 and len(a[0]) == len(a[1]):
        return True
    return False


def QSDouble(a: list):
    # a should be an array of 2 arrays with equal length
    #
    # if len(a) != 2 or len(a[0]) != len(a[1]):
    #     print('LENGTH ERROR')
    #     exit()
    length = len(a[0])
    if length <= 1:
        return a
    left = QSDouble([[a[0][i] for i in range(1, length) if a[0][i] <= a[0][0]],
                     [a[1][i] for i in range(1, length) if a[0][i] <= a[0][0]]])

    right = QSDouble([[a[0][i] for i in range(1, length) if a[0][i] > a[0][0]],
                      [a[1][i] for i in range(1, length) if a[0][i] > a[0][0]]])

    return [left[0] + [a[0][0]] + right[0], left[1] + [a[1][0]] + right[1]]

def isDigit(s: str):
    try:
        float(s)
        return True and s[0].isdigit()
    except ValueError as err:
        return False
