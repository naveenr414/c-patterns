import util
from geometry import *
from shpReader import ShapeFile
import draw
import color

colors = [color.YELLOW, color.RED,color.BLUE,color.GREEN,color.PURPLE]

fileName = "data/maryland/county/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
s = ShapeFile(fileName).shape

minX = s.polyList[0].minX
minY = s.polyList[0].minY
maxX = s.polyList[0].maxX
maxY = s.polyList[0].maxY

for i in range(len(s.polyList)):
    minX = min(minX,min(s.polyList[i].points,key=lambda x: x.x).x)
    minY = min(minY,min(s.polyList[i].points,key=lambda x: x.y).y)
    maxX = max(maxX,max(s.polyList[i].points,key=lambda x: x.x).x)
    maxY = max(maxY,max(s.polyList[i].points,key=lambda x: x.y).y)

draw.initPygame()

for i in range(len(s.polyList)):
    draw.drawPointsPygame(s.polyList[i].points,minX,minY,(maxX-minX)/2+minX,(minY+maxY)/2,fill=colors[i%len(colors)])
    

