#coding = GBK

class ConfigIni(object):
    def __init__(self, iniPath):
        self.path = iniPath
        self.values = {}
        self.readIniFile()

    def readIniFile(self):
        f = file(self.path, "r")
        lines = f.readlines()
        for line in lines:
            line = line.decode("gbk")
            idx = line.find(u"=")
            if idx!=-1:
                key = line[0:idx]
                value = line[idx+1:-1]
                self.values[key] = value
        f.close()

    def getKeyValue(self, key):
        return self.values[key]

