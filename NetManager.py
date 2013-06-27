# coding=GBK
import os
import urllib2
import socket
import time
from Config import *


##netsh interface show interface
##ipconfig /all
##HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Network\{4D36E972-E325-11CE-BFC1-08002BE10318}
##rasapi32.dll 
##
##//////////////////////////////////////////////////////////////////////////
##import os
##
##myip = os.popen("ipconfig").read()
##
##print myip
##///////////////////////////////////////////////////////////////////////////////////
##import socket
##ip_list=socket.getaddrinfo(socket.gethostname(),None)
##for i in range(len(ip_list)):
##        print (ip_list[i][4][0])
##///////////////////////////////////////////////////////////////////////////////////////


# 获取IP地址，目前只支持4
class IPTracker(object):
    def __init__(self):
        a = 0
        
    # 获取外网IP
    def getEthernetOuterIP(self):
        ip = None
        ip = self.getIpBliao()
        if ip!=None:
            isValid = self.isIPValid(ip)
            if isValid==True:
                return ip
        ip = self.getIpWhereismyip()
        if ip!=None:
            isValid = self.isIPValid(ip)
            if isValid==True:
                return ip
        return ip

    def getEthernetInnerIP(self):
        ip = socket.gethostbyname(socket.gethostname())
        return ip

    # 获取电脑上所有的IP,适用于多个连接的机器
    def getEthernetInnerIPs(self):
        names,aliases,ips = socket.gethostbyname_ex(socket.gethostname())
        return ips

    def getIpWhereismyip(self):
        url = "http://www.whereismyip.com"
        date = urllib2.urlopen(url).read()
        date = date.decode("GBK")
        keyBeg = u"\"verdana\">"
        lenKyeBeg = len(keyBeg)
        keyEnd = u"<"
        begIdx = date.find(keyBeg)
        ip = None
        if begIdx!=-1:
            endIdx = date.find(keyEnd, begIdx, len(date))
            ip = date[begIdx+lenKyeBeg:endIdx]
        return ip
            
    def getIpBliao(self):
        url = "http://www.bliao.com/ip.phtml"
        date = urllib2.urlopen(url).read()
        ip = date.decode("GBK")
        return ip

    def isIPValid(self, ip):
        try:
            iplen = len(ip)
            if iplen > 15:
                return False
            donet = u"."
            donetCount = ip.count(donet)
            if donetCount!=3:
                return False
            begIdx = 0
            endIdx = iplen
            isValid = False
            for i in range(donetCount+1):
                if i == donetCount:
                    endIdx = iplen
                else:
                    endIdx = ip.find(donet, begIdx, iplen)
                value = ip[begIdx:endIdx]
                value = (int)(value)
                if value>=0 and value<255:
                    isValid = True
                else:
                    isValid = False
                    break
                begIdx = endIdx+1
            return isValid
        except:
            return False



# 网络连接
class EthernetAdapter(object):
    def __init__(self):
        self.allName = []
        self.getAllEthernetAdapterName()

    def getAllEthernetAdapterName(self):
        ipconfigStr = os.popen("ipconfig").read()
        nameKeyBeg = "Ethernet adapter "
        self.getAllEthernetAdapterNameKeyword(ipconfigStr, nameKeyBeg)
        nameKeyBeg = "以太网适配器 "
        self.getAllEthernetAdapterNameKeyword(ipconfigStr, nameKeyBeg)
        nameKeyBeg = "无线局域网适配器 "
        self.getAllEthernetAdapterNameKeyword(ipconfigStr, nameKeyBeg)

    def getAllEthernetAdapterNameKeyword(self, ipconfigStr, nameKeyBeg):
        lenNameKeyBeg = len(nameKeyBeg)
        nameKeyEnd = ":"
        while True:
            begIdx = ipconfigStr.find(nameKeyBeg)
            if begIdx==-1:
                break
            else:
                endIdx = ipconfigStr.find(nameKeyEnd, begIdx, len(ipconfigStr))
                name = ipconfigStr[begIdx+lenNameKeyBeg:endIdx]
                name = name.decode('gbk')
                self.allName.append(name)
                ipconfigStr = ipconfigStr[endIdx+1:-1]

    def getNumEthernetAdapter(self):
        return len(self.allName)

    def getEthernetAdapterName(self, idx):
        strName = ""
        if idx>=0 and idx<self.getNumEthernetAdapter():
            strName = self.allName[idx]
        return strName

# 拨号
# EthernetDialor(u"拨号连接", u"ctnet@mycdma.cn", u"vnet.mobi")
class EthernetDialor(object):
    def __init__(self):
        self.rasdialName = "rasdial"

    def setEthernetInfo(self, ethernetName, userName, password):
        self.ethernetName = ethernetName
        self.userName = userName
        self.password = password        

    def check(self):
        cmd = self.rasdialName
        asciiCmd = cmd.encode("gbk")
        dialResult = os.popen(asciiCmd).read()
        print "check:\r\n", dialResult

    def connect(self):
        cmd = self.rasdialName + u" " \
              + "\"" + self.ethernetName + u"\" " \
              + "\"" + self.userName + u"\" " \
              + "\"" + self.rasdialName + u"\""
        asciiCmd = cmd.encode("gbk")
        dialResult = os.popen(asciiCmd).read()
        return dialResult

    def disconnect(self):
        cmd = self.rasdialName + u" " \
              + u"/DISCONNECT" + u" "
        asciiCmd = cmd.encode("gbk")
        dialResult = os.popen(asciiCmd).read()
        return dialResult


class NetManager(object):
    def __init__(self):
        self.ipTracker = IPTracker()
        self.adapter = EthernetAdapter()
        self.dialor = EthernetDialor()

    def setEthernetInfo(self, ethernetName, userName, password):
        self.dialor.setEthernetInfo(ethernetName, userName, password)

    def changeIP(self):
        print "Current IP: ", self.ipTracker.getEthernetOuterIP()
        disConResult = self.dialor.disconnect()
        print "disConResult:\r\n", disConResult
        time.sleep(5)
        conResult = self.dialor.connect()
        print "conResult:\r\n", conResult
        print " "
        time.sleep(15)


if __name__== '__main__':
    netManger = NetManager()
    config = ConfigIni("Config.ini")
    
    ethernet = config.getKeyValue(u"网络连接名称")
    user = config.getKeyValue(u"用户名")
    password = config.getKeyValue(u"密码")
    netManger.setEthernetInfo(ethernet, user, password)
    for i in range(10):
        netManger.changeIP()
