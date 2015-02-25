import math
import json

from pylab import rand
import numpy

# [ (x1, y1), (x2, y2), .... ]

class Generator(object):

    @staticmethod
    def random(num):
        return [ (x[0], x[1]) for x in rand(num, 2) ]

    @staticmethod
    def randomHorLine(num):
        data = []
        points = sorted(Generator.random(num))
        minX = points[0]
        maxX = points[len(points) - 1]
        slope = (maxX[1] - minX[1]) / (maxX[0] - minX[0])
        intercept = minX[1] - slope * minX[0]
        for point in points:
            data.append((point[0], point[0]*slope + intercept))
        return data

    @staticmethod
    def randomVertLine(num):
        data = []
        points = sorted(Generator.random(num), key=lambda tuple:tuple[1])
        minX = points[0]
        maxX = points[len(points) - 1]
        slope = (maxX[1] - minX[1]) / (maxX[0] - minX[0])
        intercept = minX[1] - slope * minX[0]
        for point in points:
            data.append(((point[1] - intercept) / slope, point[1]))
        return data

    @staticmethod
    def randomTriangle(num):
        data = []
        while len(data) < num - 3:
            point = rand(2)
            if point[1] < 2*point[0] and point[1] < -2*point[0] + 2:
                data.append((point[0], point[1]))
        data.append((1.0, 0.0))
        data.append((0.0, 0.0))
        data.append((0.5, 1.0))
        return data
       
    @staticmethod
    def randomConvexPolygon(num):
        data = [] 
        distance = numpy.random.uniform(0,.5)
        mid = (.5, .5)
        angleInc = (360/num)
        angle = 0 
        while angle < 360:
            x = mid[0] + (distance * math.cos(math.radians(angle)))
            y = mid[1] + (distance * math.sin(math.radians(angle)))
            data.append((x, y))
            angle += angleInc
        return data

    @staticmethod
    def trimetData(inJson, num=None):    
        data = []
        with open(inJson) as f:
            points = json.loads(f.read())["features"]
            for point in points[0:num]:
                data.append((
                    point["geometry"]["coordinates"][0],
                    point["geometry"]["coordinates"][1]))
        return data

if __name__ == "__main__":
    Generator.trimetStops("data/tm_stops.json")
