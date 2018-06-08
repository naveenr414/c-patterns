import turtle
import math
import copy
import pygame, sys
from pygame.locals import *
from geometry import *
import color
import util
import settings

window = 0
b = 0

def initPygame():
    global window
    
    pygame.init()
    window = pygame.display.set_mode((settings.width,settings.height),0,32)
    window.fill(color.WHITE)

def initTurtle():
    global b
    b = turtle.Turtle()

def drawPointsPygame(p,minX,minY,maxX,maxY,fill=color.BLUE):
    global window    
    
    k = copy.copy(p)
    w, h = pygame.display.get_surface().get_size()

    divide = max((maxX-minX)/w, 1/util.ratio((minY+maxY)/2)*(maxY-minY)/h)
    
    k.append(Point(p[0].x,p[0].y,1))
    k = list(map(lambda x: Point(x.x-minX,x.y-minY,x.num),k))
    k = list(map(lambda x: Point(x.x/divide,x.y/divide,x.num),k))
    k = list(map(lambda x: Point(x.x,h-1/util.ratio((minY+maxY)/2)*x.y,x.num),k))

    pointList = []
    
    for i in k:
        pointList.append([i.x,i.y])

    pygame.draw.polygon(window, fill, pointList,0)
    pygame.display.update() 

def drawPointsTurtle(p,minX,minY,maxX,maxY):
    global b

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

def drawShapePygame(s):
    drawPointsPygame(s.points,s.minX,s.minY,s.maxX,s.maxY)

def drawShapeTurtle(s):
    drawPointsTurtle(s.points,s.minX,s.minY,s.maxX,s.maxY)

