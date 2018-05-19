import turtle
import math
import copy
import pygame, sys
from pygame.locals import *
from geometry import *

pygame.init()

window = pygame.display.set_mode((500,400),0,32)

def drawPoints(p,minX,minY,maxX,maxY):
    averageX = (minX+maxX)/2
    averageY = (minY+maxY)/2

    divide = max(maxX-minX,maxY-minY)
    minus = max(averageX,averageY)
    
    scale = 200
    k = copy.copy(p)
    k.append(Point(p[0].x,p[0].y,1))
    k = list(map(lambda x: Point((x.x-minX)/divide * scale,(x.y-minY)/divide*scale,x.num),k))

    pointList = []
    for i in k:
        pointList.append([i.x,i.y])

    BLUE = (0, 0, 255)
    pygame.draw.polygon(window, BLUE, pointList,2)
    pygame.display.update()


    """
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
    """

def drawShape(s):
    drawPoints(s.points,s.minX,s.minY,s.maxX,s.maxY)

