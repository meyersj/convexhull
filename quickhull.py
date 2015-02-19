import time
from random import randint
import csv
from sets import Set
from pylab import *

BRUTE = "BruteForce"
QUICK = "QuickHull"
START = "start"
END = "end"
TIME = "{}_time"
MEM = "{}_memory"


class Runner(object):

    def __init__(self, **kwargs):
        try:
            self.writer = kwargs["writer"]
            self.name = kwargs["name"]
        except:
            pass

    # add metrics that record starting time
    # starting/ending time, memory usage and more?
    def record(self, data, phase):
        data[TIME.format(phase)] = time.clock()
    
    def run(self, name, points):
        data = {}        
        self.record(data, START)     
        output = self.algorithm(points)
        # validate output results?
        self.record(data, END)     
        self.write_results(name, data)
        return output
 
    def write_results(self, name, data):
        time_diff = (data[TIME.format(END)] - data[TIME.format(START)]) * 1000
        self.writer.writerow([self.name + name, time_diff])
    
    def sideOfLine(self, i, j, k):
            a = j[1] - i[1]
            b = i[0] - j[0]
            c = (i[0] * j[1]) - (i[1] * j[0])
            return ((a*k[0] + b*k[1]) - c)


class BruteForce(Runner):

    def algorithm(self, dataPoints):
        # NOTE what if it is a line of 3 points? should the middle point be included?
        if len(dataPoints) <= 2:
            return list(set(dataPoints))
        convexHull = Set()
        for i in dataPoints:                                # loop through all i,j pairs
            for j in dataPoints:            
                if i == j: continue                         # skip if equal
                side = 0
                for k in dataPoints:                        # compare pairs i,j to every k
                    if k == i or k == j: continue           # skip if equal
                    newSide = self.sideOfLine(i, j, k)      # check which side k is on
                    if newSide:                             # skip if k is on line
                        if not side: side = newSide         # set intial side
                        elif (side < 0 and newSide > 0) \
                            or (side > 0 and newSide < 0):
                            side = False                    # set error flag if diff side
                            break
                if side != False:                           # add points i and j to hull
                    convexHull.add(i)                       # of all k were on same side
                    convexHull.add(j)
        return list(convexHull)


class QuickHull(Runner):

    def algorithm(self, dataPoints):
        if len(dataPoints) <= 2:
            return list(set(dataPoints))
        
        left = []
        right = []
        convexHull = []
        minPoint = dataPoints[0]
        maxPoint = dataPoints[len(dataPoints)-1]
        for k in dataPoints:
            if k == minPoint or k == maxPoint: continue
            side = self.sideOfLine(minPoint, maxPoint, k)
            print k, side
            if side <= 0: left.append(k)
            else: right.append(k)
        
        convexHull += [minPoint, maxPoint]
        convexHull += self.subHull(minPoint, maxPoint, left, -1)
        convexHull += self.subHull(minPoint, maxPoint, right, 1)
        return list(set(convexHull))
    
    def subHull(self, i, j, points, startSide):
        if not points: return []
        if len(points) == 1: return [i, j, points[0]]
        
        hull = []
        left = []
        right = []
        maxPoint = self.findMaxPoint(i, j, points)
        for k in points:
            if k in [i, j, maxPoint]: continue
            sideA = self.sideOfLine(i, maxPoint, k)
            sideB = self.sideOfLine(maxPoint, j, k)
            if startSide < 0:
                if sideA < 0: left.append(k)
                elif sideB < 0: right.append(k)
            elif startSide > 0:
                if sideA > 0: left.append(k)
                elif sideB > 0: right.append(k)
        
        hull += [i, j, maxPoint]
        hull += self.subHull(i, maxPoint, left, startSide)
        hull += self.subHull(maxPoint, j, right, startSide)
        return hull

    def triangleArea(self, a, b, c):
        def toFloat(x):
            return (float(x[0]), float(x[1]))
        a = toFloat(a)
        b = toFloat(b)
        c = toFloat(c)
        A = a[0] * (b[1] - c[1])
        B = b[0] * (c[1] - a[1])
        C = c[0] * (a[1] - b[1])
        return abs((A + B + C) / 2)

    def findMaxPoint(self, i, j, points):
        maxPoint = None
        maxArea = 0
        for k in points:
            if k in [i, j]: continue
            area = self.triangleArea(i, j, k)
            if area >= maxArea:
                maxArea = area
                maxPoint = k
        return maxPoint

def generateMatrix(num, size):
    return [ (randint(0,size), randint(0,size)) for x in range(1, num) ] 


def main(output):
    csvfile = open(output, 'a')
    writer = csv.writer(csvfile)
    
    brute = BruteForce(name=BRUTE, writer=writer)
    quick = QuickHull(name=QUICK, writer=writer)
    
    data = generateMatrix(20, 100)
    quickHull = sorted(quick.algorithm(sorted(data)))
    bruteHull = sorted(brute.algorithm(data))

    if quickHull == bruteHull:
        print "MATCH!!!"
    else: print"ERROR :("
    
    plotData(data, quickHull, 100, "quick.png") 
    plotData(data, bruteHull, 100, "brute.png") 

    csvfile.close()

if __name__ == '__main__':
    main("results.csv")

