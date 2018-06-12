RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)

def toHSV(c):
    c = [i/255 for i in c]
    cMax = max(c)
    cMin = min(c)
    delta = cMax-cMin

    h = 0
    if(delta==0):
        h = 0
    elif(cMax == c[0]):
        h = 60*((c[1]-c[2])/delta % 6)
    elif(cMax == c[1]):
        h = 60 * ((c[2]-c[0])/delta + 2)
    else:
        h = 60 * ((c[0]-c[1])/delta + 4)

    s = 0
    if(cMax != 0):
        s = delta/cMax

    v = cMax

    return [h,s,v]

def toRGB(c):
    C = c[1]*c[2]
    X = C*(1-abs((c[0]/60)%2-1))
    m = c[2]-C
    color = []
    if(0<=c[0]<60):
        color = [C,X,0]
    elif(60<=c[0]<120):
        color = [X,C,0]
    elif(120<=c[0]<180):
        color = [0,C,X]
    elif(180<=c[0]<240):
        color = [0,X,C]
    elif(240<=c[0]<300):
        color = [X,0,C]
    else:
        color = [C,0,X]

    color = [(i+m)*255 for i in color]
    return color

def hexToRGB(h):
    c = []
    h = h.replace("#","")
    for i in range(0,len(h),2):
        c.append(int(h[i:i+2],16))
    return c

def gradient(start,end,value):
    start = toHSV(start)
    end = toHSV(end)

    newColor = [i[0]+value*(i[1]-i[0]) for i in zip(start,end)]
    return toRGB(newColor)
