import binascii
import struct
import random
import turtle
import copy
import math
import time
from util import toLittle
from geometry import *

class ShapeFile:
    def __init__(self,fileName,maxNum = 1000000):
        self.fileName = fileName
        self.maxNum = maxNum
        self.f = open(fileName,'rb')
        self.shape = Shape()
        self.readHeader()
        self.readBody()

    def readByte(self,num):
        temp = ""
        for i in range(num):
            h = binascii.hexlify(self.f.read(1))
            temp+=h.decode("utf8")
        return temp

    def readHeader(self):
        fileCode = self.readByte(4)
        if(fileCode!="0000270a"):
            raise ValueError("Not reading an SHP file")
        self.readByte(20)

        self.length = int(self.readByte(4),16)
        self.version = int(toLittle(self.readByte(4)),16)

        self.shapeType = int(toLittle(self.readByte(4)),16)

        #Bounding Rectangle
        mbr = toLittle(self.readByte(32))
        self.maxY = struct.unpack('d',bytes.fromhex(toLittle(mbr[0:16])))[0]
        self.maxX = struct.unpack('d',bytes.fromhex(toLittle(mbr[16:32])))[0]
        self.minY = struct.unpack('d',bytes.fromhex(toLittle(mbr[32:48])))[0]
        self.minX = struct.unpack('d',bytes.fromhex(toLittle(mbr[48:64])))[0]

        rangeZ = toLittle(self.readByte(16))
        self.maxZ = struct.unpack('d',bytes.fromhex(toLittle(rangeZ[0:16])))[0]
        self.minZ = struct.unpack('d',bytes.fromhex(toLittle(rangeZ[16:32])))[0]

        rangeM = toLittle(self.readByte(16))
        self.maxM = struct.unpack('d',bytes.fromhex(toLittle(rangeM[0:16])))[0]
        self.minM = struct.unpack('d',bytes.fromhex(toLittle(rangeM[16:32])))[0]

    def readBody(self):
        recordNumber = 1
        while(recordNumber<=self.maxNum):
            p = Polygon()
            try:
                recordNumber = int(self.readByte(4),16)
            except:
                break
            
            recordLength = int(self.readByte(4),16)
            shapeType = int(toLittle(self.readByte(4)),16)

            mbr = toLittle(self.readByte(32))
            p.maxY = struct.unpack('d',bytes.fromhex(toLittle(mbr[0:16])))[0]
            p.maxX = struct.unpack('d',bytes.fromhex(toLittle(mbr[16:32])))[0]
            p.minY = struct.unpack('d',bytes.fromhex(toLittle(mbr[32:48])))[0]
            p.minX = struct.unpack('d',bytes.fromhex(toLittle(mbr[48:64])))[0]

            numberParts = int(toLittle(self.readByte(4)),16)
            numberPoints = int(toLittle(self.readByte(4)),16)

            p.parts = []
            for i in range(numberParts):
                p.parts.append(int(toLittle(self.readByte(4)),16))

            for i in range(0,numberPoints):
                xy = toLittle(self.readByte(16))
                y = round(struct.unpack('d',bytes.fromhex(toLittle(xy[0:16])))[0],3)
                x = round(struct.unpack('d',bytes.fromhex(toLittle(xy[16:32])))[0],3)
                p.points.append(Point(x,y,i+1))

            p.calcDists()

            self.shape.polyList.append(p)



counties = ['Allegany County', 'Anne Arundel County', 'Baltimore County', 'Baltimore City', 'Calvert County', 'Caroline County', 'Carroll County', 'Cecil County', 'Charles County',
            'Dorchester County', 'Frederick County', 'Garrett County', 'Harford County', 'Howard County', 'Kent County', 'Montgomery County', "Prince George's County",
            "Queen Anne's County", "Saint Mary's County", 'Somerset County', 'Talbot County', 'Washington County', 'Wicomico County', 'Worcester County']

"""
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
        
