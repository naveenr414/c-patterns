from census import Census
from us import states
import gazetteer
import util
from geometry import *
from shpReader import ShapeFile
import draw

c = Census("a5c835dd17c5d3d22fe83e5a62d6f8fac6b3344f")

g = gazetteer.Gazetteer()
g.load(24)
stat = "B19113_001E"

tracts = c.acs5.get((stat), {'for': 'tract:*',
                       'in': 'state:{} county:031'.format(states.MD.fips)})

latitude = 0
totalPop = 0
for i in tracts:
    latitude+=float(g.find(i['county'],i['tract'])[0][-2])*int(i[stat])
    totalPop+=int(i[stat])

latitude/=totalPop
print(latitude)

fileName = "data/maryland/county/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
counties = ['Allegany County', 'Anne Arundel County', 'Baltimore County', 'Baltimore City', 'Calvert County', 'Caroline County', 'Carroll County', 'Cecil County', 'Charles County',
            'Dorchester County', 'Frederick County', 'Garrett County', 'Harford County', 'Howard County', 'Kent County', 'Montgomery County', "Prince George's County",
            "Queen Anne's County", "Saint Mary's County", 'Somerset County', 'Talbot County', 'Washington County', 'Wicomico County', 'Worcester County']
num = counties.index("Montgomery County")
s = ShapeFile(fileName,num+1).shape.polyList[num]

draw.drawShape(s)

l1 = Line(Point(-10000,latitude,1),Point(1000,latitude,2))
intersectPoints = []
for i in range(len(s.points)):
    l2 = Line(s.points[i],s.points[(i+1)%len(s.points)])

    inter = l1.intersect(l2)
    if(inter):
        inter.num = len(intersectPoints)+1
        intersectPoints.append(inter)

p1 = intersectPoints[0]
p2 = intersectPoints[1]

w = open("data.csv","w")
w.write(util.toCsv([p1,p2]))
w.close()

