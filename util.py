import math

def toLittle(b):
    """B is a string of hex values"""
    ret = ""
    for i in range(len(b)-1,-1,-2):
        ret+=b[i-1:i+1]

    return ret

def toCsv(points):
    j = "lat,lng,comment\n"
    for i in points:
        j+=str(i.y)
        j+=","
        j+=str(i.x)
        j+=","
        j+="\n"

    return j

def distLong(long1,long2,lat):
    math.cos(math.pi*lat/180)*(long2-long1) * 69.172

def distLat(lat1,lat2):
    68*(lat2-lat1)

def ratio(lat):
    #Ratio between latitude and longitude lengths
    return math.cos(math.pi*lat/180)

def calcExtrema(polyList):
    minX = polyList[0].minX
    minY = polyList[0].minY
    maxX = polyList[0].maxX
    maxY = polyList[0].maxY
    
    for i in range(len(polyList)):
        minX = min(minX,min(polyList[i].points,key=lambda x: x.x).x)
        minY = min(minY,min(polyList[i].points,key=lambda x: x.y).y)
        maxX = max(maxX,max(polyList[i].points,key=lambda x: x.x).x)
        maxY = max(maxY,max(polyList[i].points,key=lambda x: x.y).y)

    return (minX, minY, maxX, maxY)

