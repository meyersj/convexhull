import time
from random import randint
import csv
from numpy import random
from pylab import *
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


class BruteForce(Runner):

    def algorithm(self, dataPoints):
        convexHull = []
        for i in dataPoints:
            for j in dataPoints:
                if set(i) != set(j):
                    side = 0
                    for k in dataPoints:
                        if set(k) != set(i) and set(k) != set(j):
                            a = j[1] - i[1]
                            b = i[0] - j[0]
                            c = (i[0] * j[1]) - (i[1] * j[0])
                            x = ((a*k[0] + b*k[1]) - c)
                            if side == 0:
                                if x < 0:
                                    side = -1
                                elif x > 0:
                                    side = 1
                            elif x < 0 and side != -1:
                                side = -2
                                break
                            elif x > 0 and side != 1:
                                side = -2
                                break
                    if side != -2:
                        convexHull.append(tuple(i))
                        convexHull.append(tuple(j))
        return list(set(convexHull))

class QuickHull(Runner):

    def algorithm(self, points):
        minX = []
        maxX = []
        for i in points:
            if i[0] < minX: minX = i
            elif i[0] > maxX: maxX = i

        convexHull = quickHullUpper(minX, maxX, points)
        convexHull.append(quickHullLower(minX, maxX, points))
        return convexHull

    #def quickHullUpper(self, left, right, points):
        #find point creates largest area
        #construct two sets left and right
        #call again on left and right sets
        #return set of convex hull for each recurrence




def generateMatrix(num):
    return rand(num, 2) 

def plotData(data, hull, name):
    for i in data:
        plot(i[0], i[1], "b.")
    
    ylim(0,1)
    xlim(0,1) 
   
    i = 0
    while i < len(hull)-1:
        plot([hull[i][0], hull[i+1][0]], [hull[i][1], hull[i+1][1]], color='k')
        i = i + 1

    plot([hull[-1][0], hull[0][0]], [hull[-1][1], hull[0][1]], color='k')

    savefig(name)

def plotStandardData(points, hull, name):
    for i in points:
        plot(i[0], i[1], 'b.')
    for simplex in hull.simplices:
        plot(points[simplex,0], points[simplex,1], 'k-')

    savefig(name)

def sortHull(hull, points):
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

def main(output):
    csvfile = open(output, 'a')
    writer = csv.writer(csvfile)
    
    brute = BruteForce(name=BRUTE, writer=writer)
    quick = QuickHull(name=QUICK, writer=writer)

    size = 50
	#Generate set of points
    data = generateMatrix(size)
    print "\ndata:"
    print data
	#Run our brute force 
    convexHull =  brute.run("", data)
    print "\nconvexHull:"
    for vertex in convexHull:
        print vertex
	#Sort points for pretty picture
    sortedHull = sortHull(convexHull, data)
    print "\nsortedConvexHull:"
    for vertex in sortedHull:
        print vertex
	#Plot pretty picture
    plotData(data, sortedHull, "bruteforce.png")

	#Standard Library
    stdConvexHull = ConvexHull(data)
    print "\nstandardPoints:"
    for vertex in stdConvexHull.vertices:
        print stdConvexHull.points[vertex]
    plotStandardData(data, stdConvexHull, "standard.png")

    csvfile.close()


if __name__ == '__main__':
    main("results.csv")

