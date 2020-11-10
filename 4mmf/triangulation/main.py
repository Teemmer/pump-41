

class Vertex:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        if self.y == other.y:
            return self.x > other.x
        return False

    def __repr__(self):
        return "Vertex: [x={},y={}]".format(self.x, self.y)


#def make_monotone(polygon):

