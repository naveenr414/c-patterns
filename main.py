import util
from geometry import *
from shpReader import ShapeFile
import draw
import color
from census import Census
from us import states
import fips

c = Census("a5c835dd17c5d3d22fe83e5a62d6f8fac6b3344f")

colors = [color.YELLOW, color.RED,color.BLUE,color.GREEN,color.PURPLE]

fileName = "data/Maryland/County/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
s = ShapeFile(fileName).shape

minX, minY, maxX, maxY = util.calcExtrema(s.polyList)

draw.initPygame()

for i in range(len(s.polyList)):
    pop = c.acs5.state_county('B01001_001E', states.MD.fips,fips.marylandCounties[i])[0]['B01001_001E']

    time = c.acs5.state_county('B08136_001E', states.MD.fips,fips.marylandCounties[i])[0]['B08136_001E']
    amount = 0
    
    if(time):
        time/=int(pop)
        amount = (time-5)/16


    col = (amount*255,0,255-amount*255)
    draw.drawPointsPygame(s.polyList[i].points,minX,minY,maxX,maxY,fill=col)
    

