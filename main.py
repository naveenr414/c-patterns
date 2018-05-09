from shpReader import ShapeFile
import draw

fileName = "data/maryland/county/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
s = ShapeFile(fileName,1).shape.polyList[0]

draw.drawShape(s)
