import time
import random
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

    def algorithm(self, points):
        max_val = None
        for point in points:
            if max_val < point:
                max_val = point
        return max_val


class QuickHull(Runner):

    def algorithm(self, points):
        max_val = None
        for point in points:
            if max_val < point:
                max_val = point
        return max_val


def main(output):
    csvfile = open(output, 'a')
    writer = csv.writer(csvfile)
  
    brute = BruteForce(name=BRUTE, writer=writer)
    quick = QuickHull(name=QUICK, writer=writer)

    # create samples
    samples = []
    for i in range(0, 10):
        samples.append(random.sample(range(1, 100), 10))
   
    # run each sample on both brute force and quickhull
    for index, sample in enumerate(samples):
        brute.run("test" + str(index), sample)
    for index, sample in enumerate(samples):
        quick.run("test" + str(index), sample)

    csvfile.close()


if __name__ == '__main__':
    main("results.csv")

