import random

def myDet(p, q, r): #Sarrus Rule.

    sum1 = q[0] * r[1] + p[0] * q[1] + r[0] * p[1]
    sum2 = q[0] * p[1] + r[0] * q[1] + p[0] * r[1]

    return sum1 - sum2


def isRightTurn(lastThreePoints):

    (p, q, r) = lastThreePoints
    assert p != q and q != r and p != r

    if myDet(p, q, r) < 0:
        return True
    else:
        return False


def makeRandomData(numPoints, sqrLength):
    min, max = 0, sqrLength
    P = []
    for i in range(numPoints):
        rand = random.randint
        x = rand(min + 1, max - 1)
        y = rand(min + 1, max - 1)
        P.append((x, y))

    return P


epsHeader = """%%!PS-Adobe-2.0 EPSF-2.0
%%%%BoundingBox: %d %d %d %d

/r 2 def                %% radius

/circle                 %% circle, x, y, r --> -
{
    0 360 arc           %% draw circle
} def

/cross                  %% cross, x, y --> -
{
    0 360 arc           %% draw cross hair
} def

1 setlinewidth          %% thin line
newpath                 %% open page
0 setgray               %% black color

"""


def saveAsEps(P, H, boxSize, path):
    f = open(path, 'w')
    f.write(epsHeader % (0, 0, boxSize, boxSize)) #header

    format = "%3d %3d"

    if H: #path lines
        f.write("%s moveto\n" % format % H[0])
        for p in H:
            f.write("%s lineto\n" % format % p)
        f.write("%s lineto\n" % format % H[0])
        f.write("stroke\n\n")

    for p in P: #dots
        f.write("%s r circle\n" % format % p)
        f.write("stroke\n")

    f.write("\nshowpage\n") #footer


def convexHull(P):

    points = list(P)
    points.sort()

    upper = [points[0], points[1]]
    for p in points[2:]:
        upper.append(p)
        while len(upper) > 2 and not isRightTurn(upper[-3:]):
            del upper[-2]

    points.reverse()
    lower = [points[0], points[1]]
    for p in points[2:]:
        lower.append(p)
        while len(lower) > 2 and not isRightTurn(lower[-3:]):
            del lower[-2]

    del lower[0] #duplicate
    del lower[-1] #duplicate

    return tuple(upper + lower)


points = int(input("Please Enter number of points: "))
sqrlength = int(input("Please Enter the length of space: "))
path = "sample.eps"
p = makeRandomData(points, sqrlength)
c = convexHull(p)
saveAsEps(p, c, sqrlength, path)
print('Done Successfully.')