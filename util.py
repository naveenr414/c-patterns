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

