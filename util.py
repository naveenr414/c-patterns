def toLittle(b):
    """B is a string of hex values"""
    ret = ""
    for i in range(len(b)-1,-1,-2):
        ret+=b[i-1:i+1]

    return ret
