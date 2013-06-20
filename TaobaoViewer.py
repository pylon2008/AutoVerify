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
                        client = node.getBoundingClientRect()
                        if client.top >= 3500:
                            allPossibleNode += [nodeParent]
                            break
##                        allPossibleNode += [nodeParent]
    
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
    view_a_shop(ieExplorer)
