import time
from random import randint
import csv

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
                        convexHull.append(i)
                        convexHull.append(j)
        return convexHull

class QuickHull(Runner):

    def algorithm(self, points):
        max_val = None
        for point in points:
            if max_val < point:
                max_val = point
        return max_val

def generateMatrix(num):
    return [ [randint(0,100), randint(0,100)] for x in range(num) ] 

def main(output):
    csvfile = open(output, 'a')
    writer = csv.writer(csvfile)
  
    
    brute = BruteForce(name=BRUTE, writer=writer)
    quick = QuickHull(name=QUICK, writer=writer)

    data = generateMatrix(10)
    print data
    print brute.run("", data)

    # run each sample on both brute force and quickhull
    #for index, sample in enumerate(samples):
     #   brute.run("test" + str(index), sample)
    #for index, sample in enumerate(samples):
    #    quick.run("test" + str(index), sample)
    

    csvfile.close()


if __name__ == '__main__':
    main("results.csv")

