from shpReader import ShapeFile
import draw
from geometry import *

fileName = "data/maryland/county/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
counties = ['Allegany County', 'Anne Arundel County', 'Baltimore County', 'Baltimore City', 'Calvert County', 'Caroline County', 'Carroll County', 'Cecil County', 'Charles County',
            'Dorchester County', 'Frederick County', 'Garrett County', 'Harford County', 'Howard County', 'Kent County', 'Montgomery County', "Prince George's County",
            "Queen Anne's County", "Saint Mary's County", 'Somerset County', 'Talbot County', 'Washington County', 'Wicomico County', 'Worcester County']

num = counties.index("Montgomery County")
s = ShapeFile(fileName,num+1).shape.polyList[num]

averageLat = 0
for i in s.points:
    averageLat+=i.y

averageLat/=len(s.points)


l1 = Line(Point(-10000,averageLat,1),Point(10000,averageLat,2))

intersectPoints = []
for i in range(len(s.points)):
    l2 = Line(s.points[i],s.points[(i+1)%len(s.points)])

    inter = l1.intersect(l2)
    if(inter):
        inter.num = len(intersectPoints)+1
        intersectPoints.append(inter)

p1 = intersectPoints[0]
p2 = intersectPoints[1]

for i in intersectPoints:
    if(i.x<p1.x):
        p1 = i
    if(i.x>p2.x):
        p2 = i

draw.drawPoints(s.getSubset(100),s.minX,s.minY,s.maxX,s.maxY)
draw.drawPoints([p1,p2],s.minX,s.minY,s.maxX,s.maxY)
