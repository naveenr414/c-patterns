import binascii
import struct
import random
import turtle
import copy
import math
import time

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
    
    scale = 300
    k = copy.copy(p)
    k.append(p[0])
    k = list(map(lambda x: ((x[0]-averageX)/(maxX-minX),(x[1]-averageY)/(maxY-minY)),k))

    b.penup()
    b.setpos((k[0][0]*scale,k[0][1]*scale))
    b.pendown()

    currentAngle = 0
    for i in range(1,len(k)):
        angle = math.degrees(math.atan2(k[i][1]-k[i-1][1],k[i][0]-k[i-1][0]))%360
        b.left(angle-currentAngle)
        currentAngle = angle
        dist = ((k[i][1]-k[i-1][1])**2 + (k[i][0]-k[i-1][0])**2)**.5 * scale
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

while(True):
    try:
        recordNumber = int(readByte(4),16)
    except:
        break
    recordLength = int(readByte(4),16)
    shapeType = int(toLittle(readByte(4)),16)
    print("Record: "+str(recordNumber)+ " "+str(recordLength) + " "+str(shapeType))

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
        points[-1].append((x,y))
        allPoints.append((x,y))
        tempPoints.append((x,y))
        if(x<bottomLeft[0] and y<bottomLeft[1]):
            bottomLeft = (x,y)
        if(x>topRight[0] and y>topRight[1]):
            topRight = (x,y)

    num = 11

    if(recordNumber==24):
        w = open("data.csv","w")
        w.write("lat,lng,comment")
        w.write("\n")
        nums = points[num]
        for i in nums:
            w.write(str(i[::-1])[1:-1].replace(" ","")+",")
            w.write("\n")
        w.close()
        

        minX = min(allPoints, key=lambda x: x[0])[0]
        minY = min(allPoints, key=lambda x: x[1])[1]
        maxX = max(allPoints, key=lambda x: x[0])[0]
        maxY = max(allPoints, key=lambda x: x[1])[1]

        
        
