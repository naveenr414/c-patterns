"""
import util
from geometry import *
from shpReader import ShapeFile
import draw
import color
from census import Census
from us import states
import fips
import pygame
from functools import reduce

c = Census("a5c835dd17c5d3d22fe83e5a62d6f8fac6b3344f")

colors = [color.YELLOW, color.RED,color.BLUE,color.GREEN,color.PURPLE]

fileName = "data/Moco/tl_2014_24031_faces.shp"
s = ShapeFile(fileName).shape

minX, minY, maxX, maxY = util.calcExtrema(s.polyList)
minX = maxX-(maxX-minX)/4
minY = 10000
maxY = 0

for i in range(len(s.polyList)):
    tempMinX = min(s.polyList[i].points,key=lambda x: x.x).x
    tempMinY = min(s.polyList[i].points,key=lambda x: x.y).y
    tempMaxY = max(s.polyList[i].points,key=lambda x: x.y).y
    if(tempMinX>minX):
        minY = min(minY,tempMinY)
        maxY = max(maxY,tempMaxY)
    
#maxY = (minY+maxY)/4

draw.initPygame()

p1 = Point(-77.041027,38.995549,1)
p2 = Point(-77.116767,38.936892,2)
p3 = Point(-76.909548,38.892879,3)

l1 = Line(p1,p2)
l2 = Line(p1,p3)

biggestDistance = 0
smallestDistance = 7777

for i in range(len(s.polyList)):
    p = Point(1/len(s.polyList[i].points)*reduce(lambda x, y: x+y.x,(y for y in s.polyList[i].points),0),
                         1/len(s.polyList[i].points)*reduce(lambda x, y: x+y.y, (y for y in s.polyList[i].points),0),1)
    dist = min(l1.dist(p),l2.dist(p))

    cutoff = 4
    value = min(1,dist/cutoff)
    col = color.gradient(color.hexToRGB("#3A1C71"),color.hexToRGB("#FFAF7B"),value)  

    draw.drawPointsPygame(s.polyList[i].points,minX,minY,maxX,maxY,fill=col,outline=False)


print("Done Drawing")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
"""

from shpReader import ShapeFile
import draw
import util
import pygame

fileName = "data/Moco/tl_2014_24031_faces.shp"
running = True

s = ShapeFile(fileName).shape


minX, minY, maxX, maxY = util.calcExtrema(s.polyList)

draw.initPygame()

for i in range(len(s.polyList)):
    draw.drawPointsPygame(s.polyList[i].points,minX,minY,maxX, maxY,outline=False)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break

