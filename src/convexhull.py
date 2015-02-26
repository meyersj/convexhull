import time
import os
from sets import Set
import math

from pylab import clf, plot, rand, ylim, xlim, savefig
from scipy.spatial import ConvexHull as QHull

from generator import Generator as Gen

class Plotter(object):
    
    def __init__(self, outdir=""):
        self.outdir = outdir
        #if not os.path.exists(self.outdir):
        #    os.makedirs(self.outdir)

    def save(self, name, data, hull):
        clf()
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
     
    def sortHull(self, data, hull):
        difference = list(set(map(tuple,data)) - set(map(tuple,hull)))
        if not difference: return hull
        inside = difference[0]
        polar = []
        for i in hull:
            x = i[0] - inside[0]
            y = i[1] - inside[1]
            angle = math.atan2(y, x)
            polar.append(angle)
        hull = [(x,y) for (z,(x, y)) in sorted(zip(polar, hull))]
        return hull


class ConvexHull(object):

    def __init__(self):
        self.name = self.__class__.__name__
    
    def time(self, data):
        start = time.clock()
        self.algorithm(data)
        end = time.clock()
        return (time.clock() - start) * 1000
    
    def plot(self, filename, data):
        hull = self.algorithm(data)
        self.plotter.save(filename, data, hull)
    
    def sideOfLine(self, i, j, k):
        a = j[1] - i[1]
        b = i[0] - j[0]
        c = (i[0] * j[1]) - (i[1] * j[0])
        return ((a*k[0] + b*k[1]) - c)

    #returns positive if k is to the left, negative if to the right, and 0 if colinear
    def leftOfLine(self, i, j, k): 
        return j[0]-i[0])*(k[1]-i[1]) - (j[1]-i[1])*(k[0]-i[0]

class Standard(ConvexHull):
    
    def algorithm(self, points):
        stdHull = []
        for vertex in QHull(points).vertices:
            stdHull.append((points[vertex][0], points[vertex][1]))
        return stdHull
    
    def validate(self, data, results):
        return sorted(results) == sorted(self.algorithm(data))


class BruteForce(ConvexHull):

    #@profile
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
                        elif (side < 0 and newSide > 0) or (side > 0 and newSide < 0):
                            side = False
                            break
                    else:
                        pass
                        # check if distance between i and k is greater than i and j
                        # if i to j is shorter set error flag
                if side != False:
                    convexHull.add(i)
                    convexHull.add(j)
        return list(convexHull)


class QuickHull(ConvexHull):

    #@profile
    def algorithm(self, dataPoints):
        if len(dataPoints) <= 2:
            return list(set(dataPoints))
        
        left = []
        right = []
        hull = []
        minPoint = dataPoints[0]
        maxPoint = dataPoints[-1]
        for k in dataPoints:
            if k == minPoint or k == maxPoint: continue
            side = self.sideOfLine(minPoint, maxPoint, k)
            if side <= 0: left.append(k)
            else: right.append(k)
        
        hull += [minPoint, maxPoint]
        hull += self.subHull(minPoint, maxPoint, left, -1)
        hull += self.subHull(minPoint, maxPoint, right, 1)
        return list(set(hull))

    #@profile
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
                if sideB < 0: right.append(k)
            elif startSide > 0:
                if sideA > 0: left.append(k)
                if sideB > 0: right.append(k)
        
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


class GiftWrap(ConvexHull):

    #@profile
    def algorithm(self, dataPoints):
        pointOnHull = dataPoints[0]
        endPoint = dataPoints[1]
        hull = []

        while endPoint != dataPoints[0]:
            hull.append(pointOnHull)
            endPoint = dataPoints[0]
            for point in dataPoints[1:]:
                if endPoint == pointOnHull or self.leftOfLine(pointOnHull, endPoint, point) > 0:
                    endPoint = point
            pointOnHull = endPoint
        return hull
                   

if __name__ == '__main__':
    pass


