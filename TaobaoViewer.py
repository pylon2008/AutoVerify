# coding=GBK
import time, os, win32inet, win32file
from IEExplorer import *
import win32api,win32gui,win32con
import random


class TaobaoStore(object):
    def __init__(self, mainIE):
        self.mainIE = mainIE
        self.subIESet = []
        self.imgHrefNodes = []
        self.subNodes = []
        self.getImgHrefNodes()
        self.getRandomSubIE()

    def getRandomSubIE(self):
        numSubIE = random.randint(2, 4)
        numImgHrefNodes = len(self.imgHrefNodes)
        if numSubIE > numImgHrefNodes:
            numSubIE = numImgHrefNodes
##        self.imgHrefNodes.sort(key=lambda node: node.getBoundingClientRect().top)
##        for node in self.imgHrefNodes:
##            print node.getBoundingClientRect().top

        print numSubIE
        allIdxs = []
        for i in range(numSubIE):
            xx = random.randint(0, numImgHrefNodes-1)
            while True:
                if xx in allIdxs:
                    xx = random.randint(0, numImgHrefNodes-1)
                else:
                    allIdxs.append(xx)
                    print xx
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

    def createNewSubIE(self, subIdx):
        subNode = self.subNodes[subIdx]
        url = subNode.getAttribute("href")
        ie = IEExplorer()
        ie.openURL(url)
        ie.setVisible(1)
        ie.waitBusy()
        ie.waitReadyState()
        self.subIESet.append(ie)

    def getNewSubIE(self, subIdx):
        return self.subIESet[subIdx]

    def stayInSubIE(self, subIdx, stayTime):
        ie = self.getNewSubIE(subIdx)
        window = ie.getWindow()
        scrollDelta = 25
        deltaTime = 0.1
        inter = float(stayTime) / deltaTime
        inter = int(inter)
##        inter = ie.getBody().scrollHeight / scrollDelta
##        inter = inter * 9 / 10
        for i in range(inter):
            window.scrollBy(0,scrollDelta)
            ie.waitBusy()
            ie.waitReadyState()
            time.sleep(deltaTime)




    
def view_a_shop(store):
    numSubIE = store.getNumSubIE()
    for i in range(numSubIE):
        store.createNewSubIE(i)
        subIE = store.getNewSubIE(i)
        store.stayInSubIE(i, 5)
        subIE.quit()
    

    
    window = shopIE.getWindow()
    scrollDelta = 25
    inter = shopIE.getBody().scrollHeight / scrollDelta
    inter = inter * 9 / 10
    for i in range(inter):
        window.scrollBy(0,scrollDelta)
        shopIE.waitBusy()
        shopIE.waitReadyState()
        time.sleep(0.1)
        if isNodeInScreen(allPossibleNode[0], shopIE)==True:
            break

    allPossibleNode[0].focus()

    href = nodeParent.getAttribute("href")
    url = str(href)
    subIE = IEExplorer() 
    subIE.openURL(url)
    subIE.setVisible(1)
    subIE.waitBusy()
    subIE.waitReadyState()

    # move window
    subWindow = subIE.getWindow()
    for i in range(50):
        delta = -50
        subWindow.moveTo(subWindow.screenLeft-delta, subWindow.screenTop-delta)
        time.sleep(0.1)

    raw_input("请按回车键结束演示。 ")
    subIE.quit()
    time.sleep(1)
    shopIE.quit()


if __name__=='__main__':
    url = "http://hyxjf.tmall.com/?spm=a220o.1000855.w3-17818260047.2.zjWNtO&scene=taobao_shop&scene=taobao_shop"
    
    ieExplorer = IEExplorer()
    ieExplorer.openURL(url)
    ieExplorer.setVisible(1)
    ieExplorer.waitBusy()
    ieExplorer.waitReadyState()

    store = TaobaoStore(ieExplorer)
    view_a_shop(store)
