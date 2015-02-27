import os
import csv

from convexhull import Plotter, Standard, BruteForce, QuickHull, GiftWrap
from generator import Generator as Gen


BRUTE = "BruteForce"
QUICK = "QuickHull"
STD = "Standard"
GIFT = "GiftWrap"
ALGOS = [BRUTE, QUICK, GIFT, STD]

RAND = "random"
TRI = "triangle"
POLY = "polygon"
SAMPLES = [RAND, TRI, POLY]

# SET consist of multiple TESTS on the same data of the same size
TRASH = 5        # this many of the first test times are ignored
TESTS = 20       # num of times each dataset is tested
SETS = 10        # num of different datasets generated and tested for each test type

class Runner(object):

    def __init__(self, outdir="output"):
        self.outdir = outdir
        if not os.path.exists(self.outdir): os.makedirs(self.outdir)
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

   
    def plot(self, sample):
        data = Gen.generate(sample, 40)
        hull = self.std.algorithm(data) 
        self.plotter.save(sample, data, hull)

    def timeRuns(self, algo, data):
        avg = []
        #minVal = None
        #maxVal = 0
        for j in range(0, TESTS + TRASH):
            time = algo.time(data)
            #if not minVal: minVal = time
            #elif time <= minVal: minVal = time
            #if time >= maxVal: maxVal = time
            avg.append(time)
        avg = avg[TRASH:]
        return sum(avg) / float(len(avg))
        #return (sum(avg) / float(len(avg)), minVal, maxVal)

   
    def printHeader(self, i, sample):
        print "Name:", sample
        print "Suite:", i + 1, "/", SETS
        print "Tests:", TESTS
        print

    def printResults(self, brute, gift, quick, std):
        print "  ", BRUTE, brute, "ms"
        print "  ", GIFT, gift, "ms"
        print "  ", QUICK, quick, "ms"
        print "  ", STD, std, "ms"
        print

    def writeResults(self, name, results):
        with open(os.path.join(self.outdir, name), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(ALGOS)
            for i in range(0, 10):
                row = [ results[algo][i] for algo in ALGOS ]
                writer.writerow(row)

    def runSuite(self, sample, size):
        results = {BRUTE:[], QUICK:[], GIFT:[], STD:[]}
        for i in range(0, SETS):
            self.printHeader(i, sample)
            data = Gen.generate(sample, size)
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
            self.printResults(brute, gift, quick, std)
        self.writeResults(sample + str(size) + ".csv", results) 

def getBaseDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    outdir = os.path.join(getBaseDir(), "output") 
    runner = Runner(outdir=outdir)
    
    suites = []
    suites += [ (sample, 50) for sample in SAMPLES ]
    #suites += [ (sample, 100) for sample in SAMPLES ]
    #suites += [ (sample, 200) for sample in SAMPLES ]
    #suites += [ (sample, 400) for sample in SAMPLES ]
    #suites += [ (sample, 800) for sample in SAMPLES ]
   
    # run time tests
    for sample, size in suites:
        runner.runSuite(sample, size) 
    
    # generate visualization of different datasets
    #for sample in SAMPLES:
    #    runner.plot(sample)

    #runner.validate()
if __name__ == "__main__":
    main()
