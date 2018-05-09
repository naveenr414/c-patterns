from shpReader import ShapeFile
import draw

fileName = "data/maryland/county/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
counties = ['Allegany County', 'Anne Arundel County', 'Baltimore County', 'Baltimore City', 'Calvert County', 'Caroline County', 'Carroll County', 'Cecil County', 'Charles County',
            'Dorchester County', 'Frederick County', 'Garrett County', 'Harford County', 'Howard County', 'Kent County', 'Montgomery County', "Prince George's County",
            "Queen Anne's County", "Saint Mary's County", 'Somerset County', 'Talbot County', 'Washington County', 'Wicomico County', 'Worcester County']

for i, s in enumerate(ShapeFile(fileName).shape.polyList):
    area = s.calcArea()
    diamond = s.calcDiamond()
    print(counties[i]+" "+str(round(area/diamond,2)))

