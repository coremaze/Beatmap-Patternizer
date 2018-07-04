import math
def dist(p1, p2): #tuples
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
def average(l):
    return sum(l)/len(l)
def AverageAngle(a, b):
    a = a % 360
    b = b % 360
    nsum = a+b
    if nsum > 360 and nsum < 540:
        nsum = nsum % 180
    return nsum/2
