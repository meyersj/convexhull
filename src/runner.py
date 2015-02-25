import os
import csv

from convexhull import Plotter, Standard, BruteForce, QuickHull
from generator import Generator as Gen


BRUTE = "BruteForce"
QUICK = "QuickHull"
STD = "Standard"

TRASH = 5        # this many of the first test times are ignored
GEN_SIZE = 50    # size of the data sets generated
TESTS = 20       # num of times each dataset is tested
SETS = 1         # num of different datasets generated and tested for each test type

class Runner(object):

    def __init__(self, outdir=""):
        self.plotter = Plotter(outdir=outdir)
        self.brute = BruteForce()
        self.quick = QuickHull()
        self.std = Standard() 


    def validate(self):
        for i in range(0, TESTS):
            data = Gen.generate("random", GEN_SIZE)
            if not self.brute.algorithm(data):
                raise "FAILED VALIDATION:", BRUTE
        for i in range(0, TESTS):
            data = Gen.generate("random", GEN_SIZE)
            if not self.quick.algorithm(data):
                raise "FAILED VALIDATION:", QUICK
        print "VALIDATED!!"

    
    def timeRuns(self, algo, data):
        avg = []
        for j in range(0, TESTS + TRASH):
            avg.append(algo.time(data))
        avg = avg[TRASH:]
        return sum(avg) / float(len(avg))

   
    def printHeader(self, i, sample):
        print "Name:", sample
        print "Suite:", i + 1, "/", SETS
        print "Tests:", TESTS
        print

    def printResults(self, brute, quick, std):
        print "  ", BRUTE, brute, "ms"
        print "  ", QUICK, quick, "ms"
        print "  ", STD, std, "ms"
        print

    def runSuite(self, sample):
        results = {BRUTE:[], QUICK:[], STD:[]}
        for i in range(0, SETS):
            self.printHeader(i, sample)
            data = Gen.generate(sample, GEN_SIZE)
            brute = self.timeRuns(self.brute, data)
            quick = self.timeRuns(self.quick, data)
            std = self.timeRuns(self.std, data)
            results[BRUTE].append(brute)
            results[QUICK].append(quick)
            results[STD].append(quick)
            self.printResults(brute, quick, std)
             

def main(output):
    #csvfile = open(output, 'w')
    #writer = csv.writer(csvfile)
    runner = Runner(outdir="output")

    runner.runSuite("random") 
    #runner.runSuite("triangle") 
    #runner.runSuite("polygon") 
    runner.validate()
    
    #csvfile.close()


if __name__ == "__main__":
    main("results.csv")

