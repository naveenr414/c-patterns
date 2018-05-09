class Point:
    def __init__(self,x,y,n):
        self.coord = (x,y)
        self.x = self.coord[0]
        self.y = self.coord[1]
        self.num = n

    def rotate(self,angle):
        rad = angle/180 * math.pi
        self.x = self.x * math.cos(rad) - self.y * math.sin(rad)
        self.y = self.x*math.sin(rad) + self.y*math.cos(rad)
        self.coord = (x,y)

    def dist(self,p2):
        return ((self.x-p2.x)**2 + (self.y-p2.y)**2)**.5

    def __str__(self):
        return "("+str(self.x)+ ", "+str(self.y)+")"

class Polygon:
    def __init__(self):
        self.points = []
        self.dists = []
        self.parts = []
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

    def addPoint(self,p):
        self.points.append(p)

    def calcDists(self):
        p = self.points

        for i in range(len(p)):
            around = 0
            
            for j in range(-1,1):
                around+=p[(i+j)%len(p)].dist(p[(i+j+1)%len(p)])

            around-=p[(i-1)%len(p)].dist(p[(i+1)%len(p)])
            self.dists.append(around)

class Shape:
    def __init__(self):
        self.polyList = []
