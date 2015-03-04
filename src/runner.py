import os
import csv

import gspread

import config
from convexhull import Plotter, Standard, BruteForce, QuickHull, GiftWrap
from generator import Generator as Gen


BRUTE = "BruteForce"
GIFT = "GiftWrap"
QUICK = "QuickHull"
STD = "Standard"
ALGOS = [BRUTE, GIFT, QUICK, STD]

RAND = "random"
TRI = "triangle"
POLY = "polygon"
SAMPLES = [RAND, TRI, POLY]
SAMPLES = [POLY]

# SET consist of multiple TESTS on the same data of the same size
TRASH = 5        # this many of the first test times are ignored
TESTS = 20       # num of times each dataset is tested
SETS = 10        # num of different datasets generated and tested for each test type

# google spreadsheet name
SHEET = "Timings Output 2"


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
        lim={'x':(0,1), 'y':(0,1)}
        if sample.startswith("trimet"):
            data = Gen.trimet("../data/" + sample + ".json")
            if sample == "trimet_stops":
                lim={'x':(7516042,7745141), 'y':(577844,742815)}
            else:
                lim={'x':(7552870,7717026), 'y':(636210,723941)}
        else: data = Gen.generate(sample, 40)
        hull = self.std.algorithm(data) 
        self.plotter.save(sample, data, hull, lim=lim)

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

    def writeToSheets(self, name, results):
        google = gspread.login(config.EMAIL, config.PW)        
        sheet = google.open(SHEET).worksheet(name)
        
        new_cells = []
        for algo in ALGOS:
            new_cells.append(algo)
        for i in range(0, 10):
            for algo in ALGOS:
                new_cells.append(results[algo][i])

        cell_list = sheet.range('A1:D11')
        for i, cell in enumerate(cell_list):
            cell.value = new_cells[i]

        sheet.update_cells(cell_list)


    def runSuite(self, sample, size):
        results = {BRUTE:[], QUICK:[], GIFT:[], STD:[]}
        for i in range(0, SETS):
            self.printHeader(i, sample)
            data = Gen.generate(sample, size)
            #print len(data)
            #data = Gen.trimet("../data/trimet_max_stops.json", size)
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
        results[BRUTE] = [ 0 for x in range(0, 10)]
        results[GIFT] = [ 0 for x in range(0, 10)]
        self.writeToSheets(sample + str(size), results) 

def getBaseDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    outdir = os.path.join(getBaseDir(), "output") 
    runner = Runner(outdir=outdir)
    
    suites = []
    suites += [ (sample, 100) for sample in SAMPLES ]
    suites += [ (sample, 200) for sample in SAMPLES ]
    suites += [ (sample, 300) for sample in SAMPLES ]
   
    # run time tests
    for sample, size in suites:
        runner.runSuite(sample, size) 
    
    #runner.runSuite("trimet_max_stops", None)
    # generate visualization of different datasets
    #for sample in SAMPLES:
    #    runner.plot(sample)
    #runner.plot("trimet_max_stops")
    #runner.plot("trimet_stops")

    #runner.validate()
if __name__ == "__main__":
    main()

