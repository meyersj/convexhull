import time
import os
import csv
from numpy import array
from sets import Set
from pylab import plot, rand, ylim, xlim, savefig
from scipy.spatial import ConvexHull
import math

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
            self.outdir = kwargs["outdir"]
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
        except:
            pass

    # add metrics that record starting time
    # starting/ending time, memory usage and more?
    def record(self, data, phase):
        data[TIME.format(phase)] = time.clock()
    
    def run(self, name, points):
        print "TEST", name
        data = {}        
        self.record(data, START)     
        results = self.algorithm(points)
        check = self.validate(points, results) 
        print "   validate: ", check 
        self.record(data, END)     
        self.plotData(points, results, name)
        self.writeResults("test", data)
        return results

    def plotData(self, data, hull, name):
        hull = self.sortHull(hull, data)
        for i in data:
            plot(i[0], i[1], "b.")
        ylim(0,1)
        xlim(0,1) 
        i = 0
        while i < len(hull)-1:
            plot([hull[i][0], hull[i+1][0]], [hull[i][1], hull[i+1][1]], color='k')
            i = i + 1
        plot([hull[-1][0], hull[0][0]], [hull[-1][1], hull[0][1]], color='k')
        savefig(os.path.join(self.outdir, name))
     
    def sortHull(self, hull, points):
        difference = list(set(map(tuple,points)) - set(map(tuple,hull)))
        if difference == None: return hull
        inside = difference[0]
        polar = []
        for i in hull:
            x = i[0] - inside[0]
            y = i[1] - inside[1]
            angle = math.atan2(y, x)
            polar.append(angle)
        hull = [(x,y) for (z,(x, y)) in sorted(zip(polar, hull))]
        return hull
    
    def generateStd(self, points):
        stdHull = []
        for vertex in ConvexHull(points).vertices:
            stdHull.append((points[vertex][0], points[vertex][1]))
        return stdHull

    def plotStd(self, points):
        self.plotData(points, self.generateStd(points), "standard")

    def validate(self, points, results):
        return sorted(results) == sorted(self.generateStd(points))

    def writeResults(self, name, data):
        time_diff = (data[TIME.format(END)] - data[TIME.format(START)]) * 1000
        print "   time: ", time_diff
        #self.writer.writerow([self.name + name, time_diff])
    
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
        for i in dataPoints:
            for j in dataPoints:            
                if i == j: continue
                side = 0
                for k in dataPoints:
                    if k in [i, j]: continue
                    newSide = self.sideOfLine(i, j, k)
                    if newSide:
                        if not side: side = newSide
                        elif (side < 0 and newSide > 0) \
                            or (side > 0 and newSide < 0):
                            side = False
                            break
                if side != False:
                    convexHull.add(i)
                    convexHull.add(j)
        return list(convexHull)


class QuickHull(Runner):

    def algorithm(self, dataPoints):
        if len(dataPoints) <= 2:
            return list(set(dataPoints))
        
        left = []
        right = []
        hull = []
        minPoint = dataPoints[0]
        maxPoint = dataPoints[len(dataPoints)-1]
        for k in dataPoints:
            if k == minPoint or k == maxPoint: continue
            side = self.sideOfLine(minPoint, maxPoint, k)
            if side <= 0: left.append(k)
            else: right.append(k)
        
        hull += [minPoint, maxPoint]
        hull += self.subHull(minPoint, maxPoint, left, -1)
        hull += self.subHull(minPoint, maxPoint, right, 1)
        return list(set(hull))
    
    def subHull(self, i, j, points, startSide):
        if not points: return []
        if len(points) == 1: return [points[0]]
        
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


def generateMatrix(num):
    return [ (x[0], x[1]) for x in rand(num, 2) ]


def main(output):
    csvfile = open(output, 'a')
    writer = csv.writer(csvfile)

    brute = BruteForce(name=BRUTE, writer=writer, outdir="output")
    quick = QuickHull(name=QUICK, writer=writer, outdir="output")

    size = 500
    data = generateMatrix(size)
    brute.run("brute", data)
    quick.run("quick", sorted(data))
    brute.plotStd(data)    
    
    csvfile.close()


if __name__ == '__main__':
    main("results.csv")



