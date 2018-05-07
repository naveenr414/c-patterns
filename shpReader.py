import binascii
import struct
import random
import turtle
import copy
import math
import time

class Point:
    def __init__(self,x,y,n):
        self.coord = (x,y)
        self.x = self.coord[0]
        self.y = self.coord[1]
        self.dist = 0
        self.num = n

    def rotate(self,angle):
        rad = angle/180 * math.pi
        self.x = self.x * math.cos(rad) - self.y * math.sin(rad)
        self.y = self.x*math.sin(rad) + self.y*math.cos(rad)
        self.coord = (x,y)

def distance(p1,p2):
    return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**.5

b = turtle.Turtle()

def readByte(num):
    temp = ""
    for i in range(num):
        h = binascii.hexlify(f.read(1))
        temp+=h.decode("utf8")
    return temp

def toLittle(b):
    """B is a string of hex values"""
    ret = ""
    for i in range(len(b)-1,-1,-2):
        ret+=b[i-1:i+1]

    return ret

def drawPoints(p,minX,minY,maxX,maxY):

    averageX = (minX+maxX)/2
    averageY = (minY+maxY)/2

    divide = max(maxX-minX,maxY-minY)
    minus = max(averageX,averageY)

    print(p[:10])
    
    scale = 2000
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
        dist = distance(k[i],k[i-1])* scale
        b.forward(dist)

    b.left(360-currentAngle)


fileName = "data/maryland/county/Maryland_Physical_Boundaries__County_Boundaries_Generalized.shp"
f = open(fileName,'rb')

fileCode = readByte(4)
if(fileCode!="0000270a"):
    raise ValueError("Not reading an SHP file")

readByte(20)

length = readByte(4)
length = int(length,16)
print("Length is "+str(length))

version = int(toLittle(readByte(4)),16)
print("Version is",version)


shapeType = int(toLittle(readByte(4)),16)
print(shapeType)

mbr = toLittle(readByte(32))
maxY = struct.unpack('d',bytes.fromhex(toLittle(mbr[0:16])))[0]
maxX = struct.unpack('d',bytes.fromhex(toLittle(mbr[16:32])))[0]
minY = struct.unpack('d',bytes.fromhex(toLittle(mbr[32:48])))[0]
minX = struct.unpack('d',bytes.fromhex(toLittle(mbr[48:64])))[0]

print([minX,minY],[maxX,maxY])

rangeZ = toLittle(readByte(16))
maxZ = struct.unpack('d',bytes.fromhex(toLittle(rangeZ[0:16])))[0]
minZ = struct.unpack('d',bytes.fromhex(toLittle(rangeZ[16:32])))[0]

rangeM = toLittle(readByte(16))
maxM = struct.unpack('d',bytes.fromhex(toLittle(rangeM[0:16])))[0]
minM = struct.unpack('d',bytes.fromhex(toLittle(rangeM[16:32])))[0]

bottomLeft = (10000,100000)
topRight = (-10000,-10000)
points = []
allPoints = []

counties = ['Allegany County', 'Anne Arundel County', 'Baltimore County', 'Baltimore City', 'Calvert County', 'Caroline County', 'Carroll County', 'Cecil County', 'Charles County',
            'Dorchester County', 'Frederick County', 'Garrett County', 'Harford County', 'Howard County', 'Kent County', 'Montgomery County', "Prince George's County",
            "Queen Anne's County", "Saint Mary's County", 'Somerset County', 'Talbot County', 'Washington County', 'Wicomico County', 'Worcester County']
while(True):
    try:
        recordNumber = int(readByte(4),16)
    except:
        break
    recordLength = int(readByte(4),16)
    shapeType = int(toLittle(readByte(4)),16)
    #print("Record: "+str(recordNumber)+ " "+str(recordLength) + " "+str(shapeType))
    print("County Name: "+counties[recordNumber-1])

    mbr = toLittle(readByte(32))
    maxY = struct.unpack('d',bytes.fromhex(toLittle(mbr[0:16])))[0]
    maxX = struct.unpack('d',bytes.fromhex(toLittle(mbr[16:32])))[0]
    minY = struct.unpack('d',bytes.fromhex(toLittle(mbr[32:48])))[0]
    minX = struct.unpack('d',bytes.fromhex(toLittle(mbr[48:64])))[0]

    numberParts = int(toLittle(readByte(4)),16)
    #print("Number of parts is "+str(numberParts))

    numberPoints = int(toLittle(readByte(4)),16)
    #print("Number of points is "+str(numberPoints))

    partIndexes = []
    for i in range(numberParts):
        partIndexes.append(int(toLittle(readByte(4)),16))

    tempPoints = []
    points.append([])
    for i in range(0,numberPoints):
        xy = toLittle(readByte(16))
        y = round(struct.unpack('d',bytes.fromhex(toLittle(xy[0:16])))[0],3)
        x = round(struct.unpack('d',bytes.fromhex(toLittle(xy[16:32])))[0],3)
        points[-1].append(Point(x,y,i+1))
        allPoints.append(Point(x,y,i+1))

    for i in range(0,numberPoints):
        points[-1][i].dist = distance(points[-1][(i-1)%numberPoints],points[-1][(i)
                            %numberPoints])+distance(points[-1][(i)%numberPoints],points[-1][(i+1)
                            %numberPoints]) - distance(points[-1][(i-1)%numberPoints],
                            points[-1][(i+1)%numberPoints])


    minX = 10000
    maxX = -1000000
    minY = 1000000
    maxY = -10000000
    
    for i in range(numberPoints):
        p = copy.deepcopy(points[-1][i])
        p.rotate(45)
        minX = min(p.x,minX)
        maxX = max(p.x,maxX)
        minY = min(p.y,minY)
        maxY = max(p.y,maxY)

    boundingArea = (max(maxX-minX,maxY-minY))**2

    realArea = 0
    for i in range(numberPoints):
        realArea+=points[-1][i].x * points[-1][(i+1)%numberPoints].y
        realArea-=points[-1][i].y * points[-1][(i+1)%numberPoints].x

    realArea = 1/2*abs(realArea)
    print("Diamond percentage "+str(round(realArea/boundingArea,2)))
    

    """
    if(recordNumber==16):

        nums = points[recordNumber-1]
        w = open("data.csv","w")
        w.write("lat,lng,comment")
        w.write("\n")

        for i in nums:
            w.write(str(i.coord[::-1])[1:-1].replace(" ","")+",")
            w.write("\n")
        w.close()

        
        minX = min(allPoints, key=lambda x: x.x).x
        minY = min(allPoints, key=lambda x: x.y).y
        maxX = max(allPoints, key=lambda x: x.x).x
        maxY = max(allPoints, key=lambda x: x.y).y

        nums = sorted(sorted(points[recordNumber-1],key=lambda x: x.dist)[-100:],key=lambda x: x.num)
        p = [(min(nums, key=lambda x: x.y).y, -77.117),
             (39.118, min(nums, key=lambda x: x.x).x), (39.339,-77.187), (39.126, -76.893)]
        for i in range(len(p)):
            p[i] = Point(p[i][1],p[i][0],i)

        drawPoints(nums,minX,minY,maxX,maxY)
        drawPoints(p,minX,minY,maxX,maxY)
    """
        
