import binascii
import struct

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

fileName = "data/cb_2017_us_state_20m/cb_2017_us_state_20m.shp"
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

recordNumber = int(readByte(4),16)
recordLength = int(readByte(4),16)
shapeType = int(toLittle(readByte(4)),16)
print("Record: "+str(recordNumber)+ " "+str(recordLength) + " "+str(shapeType))

mbr = toLittle(readByte(32))
maxY = struct.unpack('d',bytes.fromhex(toLittle(mbr[0:16])))[0]
maxX = struct.unpack('d',bytes.fromhex(toLittle(mbr[16:32])))[0]
minY = struct.unpack('d',bytes.fromhex(toLittle(mbr[32:48])))[0]
minX = struct.unpack('d',bytes.fromhex(toLittle(mbr[48:64])))[0]

numberParts = int(toLittle(readByte(4)),16)
print("Number of parts is "+str(numberParts))

numberPoints = int(toLittle(readByte(4)),16)
print("Number of points is "+str(numberPoints))

partIndexes = []
for i in range(numberParts):
    partIndexes.append(int(toLittle(readByte(4)),16))

for i in range(0,partIndexes[1]):
    xy = toLittle(readByte(16))
    y = struct.unpack('d',bytes.fromhex(toLittle(xy[0:16])))[0]
    x = struct.unpack('d',bytes.fromhex(toLittle(xy[16:32])))[0]
    print((x,y),end=", ")
