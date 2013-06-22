# coding=GBK
import time, os, win32inet, win32file
import win32api,win32gui,win32con, traceback
import random
from IEExplorer import *
from IEProxy import *

NUM_BAT_TAOBAO_BAOBEI_VIEW = 2                  # 一次浏览宝贝的数量
NUM_SUB_PAGE_MIN = 1                            # 子页面数量最小值
NUM_SUB_PAGE_MAX = 1                            # 子页面数量最大值
TIME_PROXY_CHANGE = 30                          # 切换IP地址总时间

class TaobaoBaobei(object):
    def __init__(self, mainIE):
        self.mainIE = mainIE
        self.subIESet = []
        self.imgHrefNodes = []
        self.subNodes = []
        self.timeBegOp = None                   # 开始操作宝贝的起点时间，从开始滚动开始

    def getRandomSubIE(self):
        numSubIE = random.randint(NUM_SUB_PAGE_MIN, NUM_SUB_PAGE_MAX)
        numImgHrefNodes = len(self.imgHrefNodes)
        if numSubIE > numImgHrefNodes:
            numSubIE = numImgHrefNodes
##        self.imgHrefNodes.sort(key=lambda node: node.getBoundingClientRect().top)
##        for node in self.imgHrefNodes:
##            print node.getBoundingClientRect().top

        allIdxs = []
        for i in range(numSubIE):
            xx = random.randint(0, numImgHrefNodes-1)
            while True:
                if xx in allIdxs:
                    xx = random.randint(0, numImgHrefNodes-1)
                else:
                    allIdxs.append(xx)
                    break
                
        for i in range(len(allIdxs)):
            self.subNodes.append( self.imgHrefNodes[allIdxs[i]] )

    def getImgHrefNodes(self):
        body = self.mainIE.getBody()
        nodesImg = getSubNodesByTag(body, "img")
        for node in nodesImg:
            nodeParent = node.parentElement
            if nodeParent!=None:
                if nodeParent.tagName==u"a" or nodeParent.tagName==u"A":
                    href = nodeParent.getAttribute("href")
                    if type(href)==unicode and href!=u"":
                        if u"detail" in href:
                            self.imgHrefNodes.append(nodeParent)
##                            self.imgHrefNodes += [nodeParent]
##                            client = node.getBoundingClientRect()
##                            if client.top >= 3500:
##                                self.imgHrefNodes += [nodeParent]
##                                break

    def getNumSubIE(self):
        return len(self.subNodes)

    def getTimeBegOp(self):
        return self.timeBegOp

    def createNewSubIE(self, subIdx):
        subNode = self.subNodes[subIdx]
        url = subNode.getAttribute("href")
        ie = IEExplorer()
        ie.openURL(url)
        ie.setVisible(1)
        self.subIESet.append(ie)

    def getMainIE(self):
        return self.mainIE
    
    def getNewSubIE(self, subIdx):
        return self.subIESet[subIdx]

    def openCurBaobei(self):
        self.getImgHrefNodes()
        self.getRandomSubIE()
        self.timeBegOp = datetime.datetime.now()
        
        numSubIE = self.getNumSubIE()
        for subIdx in range(numSubIE):
            # 回宝贝界面
            while self.mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                self.mainIE.stop()
                time.sleep(0.1)
            self.mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
            self.mainIE.setForeground()
            self.mainIE.resizeMax()
            while self.mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                self.mainIE.stop()
                time.sleep(0.1)
            self.mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)

            # 打开子页面
            subNode = self.subNodes[subIdx]
            self.mainIE.scrollToNode(subNode)
            subNode.focus()
            self.createNewSubIE(subIdx)

            # 滚动子页面
            subIE = self.getNewSubIE(subIdx)
            while subIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                subIE.stop()
                time.sleep(0.1)
            isReady = subIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
            timeOut = random.randint(3, 5)
            subIE.stayInSubPage(timeOut)

            if subIdx != numSubIE-1:
                time.sleep(2)           


class TaobaoViewer(object):
    def __init__(self):
        self.mainIE = []                                    # 本次浏览集合
        self.baobeiSet = []                                 # 配置文件中所有的宝贝集合
        self.numBaobei = NUM_BAT_TAOBAO_BAOBEI_VIEW         # 一次打开的宝贝的数量

        # 读取所有宝贝
        self.file = file('UrlConfig.txt', 'r')
        while True:
            line = self.file.readline()
            if len(line)==0:
                break
            rr = line.split(' ')
            numVisit = int(rr[0])
            url = rr[1]
            self.baobeiSet.append( [numVisit,url] )

        # 随机抽取访问对象
        self.randomVisit = []
        for i in range(self.numBaobei):
            while True:
                rr = random.randint(0, len(self.baobeiSet)-1)
                if rr not in self.randomVisit:
                    if self.baobeiSet[rr][0] > 0:
                        self.randomVisit.append(rr)
                        break
        print self.randomVisit
        
    def numVisit(self):
        return len(self.randomVisit)

    def createBaobei(self, visitIdx):
        realIdx = self.randomVisit[visitIdx]
        self.baobeiSet[realIdx][0] -= 1
        url = self.baobeiSet[realIdx][1]
        ieExplorer = IEExplorer()
        ieExplorer.openURL(url)
        ieExplorer.setVisible(1)
        store = TaobaoBaobei(ieExplorer)
        self.mainIE.append(store)

    def getBaobei(self, visitIdx):
        return self.mainIE[visitIdx]

    def unInit(self):
        self.file.close()

    def closeAllIE(self):
        numVisitBaobei = self.numVisit()
        for mainIdx in range(numVisitBaobei):
            print "mainIdx: ", mainIdx,
            baobei = self.getBaobei(mainIdx)
            print ", type(baobei): ", type(baobei),
            print ", baobei.getNumSubIE(): ", baobei.getNumSubIE()
            for subIdx in range(baobei.getNumSubIE()):
                subIE = baobei.getNewSubIE(subIdx)
                print "subIdx: ", subIdx,
                print ", type(subIE): ", type(subIE)
                while subIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                    subIE.stop()
                    time.sleep(0.1)
                subIE.setForeground()
                time.sleep(IE_INTERVAL_TIME_CLOSE)
                subIE.quit()
            while baobei.getMainIE().waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                baobei.getMainIE().stop()
                time.sleep(0.1)
            baobei.getMainIE().setForeground()
            time.sleep(IE_INTERVAL_TIME_CLOSE)
            baobei.getMainIE().quit()


def view_3_baobei():
    viewer = TaobaoViewer() 

    # 打开3个宝贝界面
    numVisitBaobei = viewer.numVisit()
    for idx in range(numVisitBaobei):
        viewer.createBaobei(idx)

    # 打开宝贝界面的子页面，并滚动子页面
    timeBegOp = None
    for idx in range(numVisitBaobei):
        baobei = viewer.getBaobei(idx)
        mainIE = baobei.getMainIE()
        while mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
            mainIE.stop()
            time.sleep(0.1)
        mainIE.setForeground()
        mainIE.resizeMax()
        while mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
            mainIE.stop()
            time.sleep(0.1)
        mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
        baobei.openCurBaobei()
        if idx==0:
            timeBegOp = baobei.getTimeBegOp()

    # 停顿
    timePass = (datetime.datetime.now() - timeBegOp).seconds
    timeSleep = 320 - timePass
    if timeSleep <= 45:
        timeSleep = 45
    print "timeSleep: ", timeSleep
    timeSleep = 20
    time.sleep(timeSleep)

    # 关闭所有宝贝
    viewer.closeAllIE()

    # write URL config


if __name__=='__main__':
    ieProxy = IEProxy("proxy.txt")

    batIdx = 0
    while True:
        print "\r\n\r\nbatIdx: ", batIdx
        view_3_baobei()
##    try:
##        view_3_baobei()
##    except:
##        closeAllRunningIE()
        
        # change IP
        timeProxyBeg = datetime.datetime.now()
        ieProxy.changeProxy()
        timeProxyEnd = datetime.datetime.now()
        deltaTime = (timeProxyEnd - timeProxyBeg).seconds
        print "change proxy time: ", deltaTime
        sleepTime = TIME_PROXY_CHANGE - deltaTime
        if sleepTime < 10:
            sleepTime = 10
        time.sleep(sleepTime)
        batIdx += 1



# TODO
#1.URL配置文件要记录到文件
#2.代理的设置时刻可改在停顿时
#3.找新代理点
