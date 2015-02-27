import os
import csv

from convexhull import Plotter, Standard, BruteForce, QuickHull, GiftWrap
from generator import Generator as Gen


BRUTE = "BruteForce"
QUICK = "QuickHull"
STD = "Standard"
GIFT = "GiftWrap"

GEN_SIZE = 50   # size of the data sets generated
TRASH = 5        # this many of the first test times are ignored
TESTS = 10       # num of times each dataset is tested
SETS = 10        # num of different datasets generated and tested for each test type

# SETS consist of multiple TESTS of GEN_SIZE

class Runner(object):

    def __init__(self, outdir="output", outfile="results.csv"):
        self.outfile = os.path.join(outdir, outfile)
        self.plotter = Plotter(outdir=outdir)
        self.brute = BruteForce()
        self.quick = QuickHull()
        self.gift = GiftWrap() 
        self.std = Standard() 

    def validate(self):
        for i in range(0, TESTS):
            data = Gen.generate("random", GEN_SIZE)
            results = self.brute.algorithm(data)
            if not self.std.validate(data, results):
                raise "FAILED VALIDATION:", BRUTE
        for i in range(0, TESTS):
            data = Gen.generate("random", GEN_SIZE)
            results = self.quick.algorithm(data)
            if not self.std.validate(data, results):
                raise "FAILED VALIDATION:", QUICK
        for i in range(0, TESTS):
            data = Gen.generate("random", GEN_SIZE)
            results = self.gift.algorithm(data)
            if not self.std.validate(data, results):
                raise "FAILED VALIDATION:", GIFT
        print "VALIDATED!!"

   
    def plot(self):
        data = Gen.generate("random", GEN_SIZE)
        quick = self.quick.algorithm(data)
        brute = self.brute.algorithm(data)
        gift = self.gift.algorithm(data)
        std = self.std.algorithm(data)

        self.plotter.save(QUICK, data, quick)
        self.plotter.save(BRUTE, data, brute)
        self.plotter.save(STD, data, std)
        self.plotter.save(GIFT, data, gift)


    def timeRuns(self, algo, data):
        avg = []
        minVal = None
        maxVal = 0
        for j in range(0, TESTS + TRASH):
            time = algo.time(data)
            if not minVal: minVal = time
            elif time <= minVal: minVal = time
            if time >= maxVal: maxVal = time
            avg.append(time)
        avg = avg[TRASH:]
        return sum(avg) / float(len(avg))
        #return (sum(avg) / float(len(avg)), minVal, maxVal)

   
    def printHeader(self, i, sample):
        print "Name:", sample
        print "Suite:", i + 1, "/", SETS
        print "Tests:", TESTS
        print

    def printResults(self, brute, quick, gift, std):
        print "  ", BRUTE, brute, "ms"
        print "  ", QUICK, quick, "ms"
        print "  ", GIFT, gift, "ms"
        print "  ", STD, std, "ms"
        print

    def writeResults(self, name, results):
        with open(self.outfile, 'w') as f:
            writer = csv.writer(f)
            for algo in [BRUTE, QUICK, GIFT, STD]:
                writer.writerow([algo, name] + results[algo])

    def runSuite(self, sample):
        results = {BRUTE:[], QUICK:[], GIFT:[], STD:[]}
        for i in range(0, SETS):
            self.printHeader(i, sample)
            data = Gen.generate(sample, GEN_SIZE)
            # run tests
            brute = self.timeRuns(self.brute, data)
            quick = self.timeRuns(self.quick, data)
            gift = self.timeRuns(self.gift, data)
            std = self.timeRuns(self.std, data)
            # save avg
            results[BRUTE].append(brute)
            results[QUICK].append(quick)
            results[GIFT].append(gift)
            results[STD].append(std)
            self.printResults(brute, quick, gift, std)
        self.writeResults(sample, results) 

def main(outfile):
    outdir = "../output"
    test = "random"
    runner = Runner(outdir=outdir, outfile=test+"200.csv")
    
    #runner.runSuite(test) 
    #runner.validate()
    runner.plot()

if __name__ == "__main__":
    main("results.csv")

