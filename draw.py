import turtle
import math
import copy
from geometry import *

b = turtle.Turtle()

def drawPoints(p,minX,minY,maxX,maxY):
    averageX = (minX+maxX)/2
    averageY = (minY+maxY)/2

    divide = max(maxX-minX,maxY-minY)
    minus = max(averageX,averageY)
    
    scale = 300
    k = copy.copy(p)
    k.append(Point(p[0].x,p[0].y,1))
    k = list(map(lambda x: Point((x.x-averageX)/divide,(x.y-averageY)/divide,x.num),k))

    b.penup()
    b.setpos((k[0].x*scale,k[0].y*scale))
    b.pendown()

    currentAngle = 0
    for i in range(1,len(k)):
        angle = math.degrees(math.atan2(k[i].y-k[i-1].y,k[i].x-k[i-1].x))%360
        b.left(angle-currentAngle)
        currentAngle = angle
        dist = k[i].dist(k[i-1])* scale
        b.forward(dist)

    b.left(360-currentAngle)

def drawShape(s):
    drawPoints(s.points,s.minX,s.minY,s.maxX,s.maxY)

