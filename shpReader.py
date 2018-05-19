import binascii
import struct
import random
import turtle
import copy
import math
import time
from util import toLittle
from geometry import *

PRECISION = 2

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
                y = round(struct.unpack('d',bytes.fromhex(toLittle(xy[0:16])))[0],PRECISION)
                x = round(struct.unpack('d',bytes.fromhex(toLittle(xy[16:32])))[0],PRECISION)
                p.points.append(Point(x,y,i+1))

            p.calcDists()

            self.shape.polyList.append(p)
        
