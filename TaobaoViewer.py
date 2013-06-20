# coding=GBK
import time, os, win32inet, win32file
from IEExplorer import *
import win32api,win32gui,win32con


def view_a_shop(shopIE):
    body = shopIE.getBody()
    nodesImg = getSubNodesByTag(body, "img")
    allPossibleNode = []
    for node in nodesImg:
        nodeParent = node.parentElement
        if nodeParent!=None:
            if nodeParent.tagName==u"a" or nodeParent.tagName==u"A":
                href = nodeParent.getAttribute("href")
                if type(href)==unicode and href!=u"":
                    if u"detail" in href:
                        allPossibleNode += [nodeParent]
    
    window = shopIE.getWindow()
    scrollDelta = 30
    inter = shopIE.getBody().scrollHeight / scrollDelta
    for i in range(inter):
        window.scrollBy(0,scrollDelta)
        time.sleep(0.1)
        if isNodeInScreen(allPossibleNode[0], shopIE)==True:
            break
    window.moveTo(window.screenLeft-100, window.screenTop-100)

##    allPossibleNode[0].click()
##    allPossibleNode[0].focus()
    print allPossibleNode[0]



if __name__=='__main__':
    url = "http://hyxjf.tmall.com/?spm=a220o.1000855.w3-17818260047.2.zjWNtO&scene=taobao_shop&scene=taobao_shop"
    
    ieExplorer = IEExplorer()
    ieExplorer.openURL(url)
    ieExplorer.setVisible(1)
    ieExplorer.waitBusy()
    ieExplorer.waitReadyState()
    view_a_shop(ieExplorer)
