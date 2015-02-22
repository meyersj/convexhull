from pylab import rand

# [ (x1, y1), (x2, y2), .... ]

class Generator(object):

    def random(self, num):
        return [ (x[0], x[1]) for x in rand(num, 2) ]

    def randomHorLine(self, num):
        data = []
        points = sorted(self.random(num))
        minX = points[0]
        maxX = points[len(points) - 1]
        slope = (maxX[1] - minX[1]) / (maxX[0] - minX[0])
        intercept = minX[1] - slope * minX[0]
        for point in points:
            data.append((point[0], point[0]*slope + intercept))
        return data

    def randomVertLine(self, num):
        data = []
        points = sorted(self.random(num), key=lambda tuple:tuple[1])
        minX = points[0]
        maxX = points[len(points) - 1]
        slope = (maxX[1] - minX[1]) / (maxX[0] - minX[0])
        intercept = minX[1] - slope * minX[0]
        for point in points:
            data.append(((point[1] - intercept) / slope, point[1]))
        return data

    def randomTriangle(self, num):
        data = []
        while len(data) < num - 3:
            point = rand(2)
            if point[1] < 2*point[0] and point[1] < -2*point[0] + 2:
                data.append((point[0], point[1]))
        data.append((1.0, 0.0))
        data.append((0.0, 0.0))
        data.append((0.5, 1.0))
        return data
        
