import time
from random import randint
import csv
from pylab import *
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
                if i != j:
                    side = 0
                    for k in dataPoints:
                        if k != i and k != j:
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




def generateMatrix(num, size):
    return [ [randint(0,size), randint(0,size)] for x in range(num) ] 

def plotData(data, hull, dataRange):
    for i in data:
        plot(i[0], i[1], "b.")
    
    ylim(0,dataRange)
    xlim(0,dataRange) 
    
    i = 0
    while i < len(hull)-1:
        plot([hull[i][0], hull[i+1][0]], [hull[i][1], hull[i+1][1]], color='k')
        i = i + 1

    plot([hull[-1][0], hull[0][0]], [hull[-1][1], hull[0][1]], color='k')


    savefig("foo.png")

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
    dataRange = 100
    data = generateMatrix(size, dataRange)
    print data
    convexHull =  brute.run("", data)
    print convexHull
    sortedHull = sortHull(convexHull, data)
    print sortedHull
    plotData(data, sortedHull, dataRange)
    csvfile.close()


if __name__ == '__main__':
    main("results.csv")

