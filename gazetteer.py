import bisect

class Gazetteer:
    def __init__(self):
        pass

    def load(self,stateNumber):
        self.stateNumber = stateNumber
        self.f = open("data/gazetteer/2017_gaz_tracts_"+str(stateNumber)+".txt").read().split("\n")[2:-1]
        self.geoList = []
        for i in range(len(self.f)):
            self.f[i] = self.f[i].split("\t")
            self.geoList.append(self.f[i][1])

    def find(self,countyNumber,tractNumber):
        geoid = str(self.stateNumber)+str(countyNumber)+str(tractNumber)
        intersectPoint = bisect.bisect_left(self.geoList,geoid)

        retList = []
        i = intersectPoint
        while(i>=0 and self.geoList[i]==geoid):
            retList.append(self.f[i])
            i-=1

        i = intersectPoint+1
        while(i<len(self.geoList) and self.geoList[i]==geoid):
            retList.append(self.f[i])
            i+=1

        return retList
