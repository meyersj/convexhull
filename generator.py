from pylab import rand

# [ (x1, y1), (x2, y2), .... ]

class Generator(object):

    def random(self, num):
        return [ (x[0], x[1]) for x in rand(num, 2) ]


