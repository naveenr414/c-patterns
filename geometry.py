import math
import copy
import numpy as np
from util import *

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

class Line:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def intersect(self,l2):
        x1,y1 = self.p1.x, self.p1.y
        x2,y2 = self.p2.x, self.p2.y
        x,y = l2.p1.x, l2.p1.y
        xB,yB = l2.p2.x, l2.p2.y
        
        dx1 = x2-x1
        dy1 = y2-y1

        dx = xB-x
        dy = yB-y

        det = (-dx1 * dy + dy1 * dx)
        if(abs(det)<.0001):
            return False

        DETinv = 1.0/det

        r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))

        s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))

        if(0<r<1 and 0<s<1):
            xi = (x1 + r*dx1 + x + s*dx)/2.0
            yi = (y1 + r*dy1 + y + s*dy)/2.0
            return Point(xi,yi,1)
        else:
            return False

    def dist(self,p3):
        A = np.array((distLong(0,self.p1.x,self.p1.y),distLat(0,self.p1.y)))
        B = np.array((distLong(0,self.p2.x,self.p2.y),distLat(0,self.p2.y)))
        P = np.array((distLong(0,p3.x,p3.y),distLat(0,p3.y)))


        if all(A == P) or all(B == P):
            return 0
        if np.arccos(np.dot((P - A) / np.linalg.norm(P - A), (B - A) / np.linalg.norm(B - A))) > np.pi / 2:
            return np.linalg.norm(P - A)
        if np.arccos(np.dot((P - B) / np.linalg.norm(P - B), (A - B) / np.linalg.norm(A - B))) > np.pi / 2:
            return np.linalg.norm(P - B)
        return np.linalg.norm(np.cross(A-B,A-P))/np.linalg.norm(B-A)

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

    def calcArea(self):
        area = 0
        for i in range(len(self.points)):
            area+=self.points[i].x * self.points[(i+1)%len(self.points)].y
            area-=self.points[i].y * self.points[(i+1)%len(self.points)].x
        area = 1/2 * abs(area)
        area*=111.111**2 * math.cos(math.pi/180*self.points[0].y)
        return area

    def calcDiamond(self):
        angle = 45 * math.pi/180
        tempPoints = copy.deepcopy(self.points)
        total = Point(0,0,1)
        for i in range(len(tempPoints)):
            total.x+=tempPoints[i].x
            total.y+=tempPoints[i].y
            
        total.x/=len(tempPoints)
        total.y/=len(tempPoints)

        for i in range(len(tempPoints)):
            s,c = math.sin(angle), math.cos(angle)

            tempPoints[i].x-=total.x
            tempPoints[i].y-=total.y

            tempPoints[i].x=total.x + (tempPoints[i].x*c - tempPoints[i].y*s)
            tempPoints[i].y=total.y + (tempPoints[i].x*s + tempPoints[i].y*c)   

        minX = 1000000
        maxX = -100000
        minY = 1000000
        maxY = -1000000

        for i in range(len(tempPoints)):
            minX = min(minX,tempPoints[i].x)
            maxX = max(maxX,tempPoints[i].x)
            minY = min(minY,tempPoints[i].y)
            maxY = max(maxY,tempPoints[i].y)

        
        area = max(maxX-minX)*(maxY-minY)
        area*=111.111**2 * math.cos(math.pi/180 * self.points[0].y)

        return area

    def getSubset(self,select):
        bestPoints = sorted(self.points,key=lambda x: self.dists[self.points.index(x)])[-select:]
        return sorted(bestPoints, key=lambda x: x.num)
    
class Shape:
    def __init__(self):
        self.polyList = []
