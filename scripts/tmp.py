from datetime import datetime


def dateTest():
    month_ago = datetime.now()
    print(month_ago)
    month_ago = month_ago.replace(microsecond=0, month=month_ago.month-1)
    print(month_ago)


def QuickSort(a):
    if len(a) <= 1:
        return a
    pilot = (len(a)) // 2
    right = []
    left = []
    for i in range(len(a)):
        if i == pilot:
            continue
        if a[i] > a[pilot]:
            right.append(a[i])
        else:
            left.append(a[i])
    pilot = list([a[pilot]])
    return QuickSort(left) + pilot + QuickSort(right)

n = int(input())
arr = [int(i) for i in input().split()]
arr = QuickSort(arr)
for i in range(len(arr)):
    print(arr[i], end=" ")


def QSForDouble(a):
    if len(a) <= 1:
        return a
    pilot = len(a) // 2
    right = [[], []]
    left = [[], []]
    for i in range(len(a)):
        if i == pilot:
            continue
        if a[1][i] > a[1][pilot]:
            right[0].append(a[0][i])
            right[1].append(a[1][i])
        else:
            left[0].append(a[0][i])
            left[1].append(a[1][i])
    qsl = QSForDouble(left)
    qsr = QSForDouble(right)
    return [[qsl[0].append(a[0][pilot]) + qsr[0]], [qsl[1].append(a[1][pilot]) + qsr[1]]]


dateTest()