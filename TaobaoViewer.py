# coding=GBK
import time, os, win32inet, win32file
from IEExplorer import *
import win32api,win32gui,win32con

def input_qq_info(ie6, imgVerifior):
    humanInterval = 0.2

    body = ie6.getBody()
    
    nodesInput = getSubNodesByTag(body, "input")

    
    node = getNodeByAttr(nodesInput, 'id', 'nick')
    node.click()
    node.focus()
    enumHumanInput(node, 'pylon2888')

    node = getNodeByAttr(nodesInput, 'id', 'password')
    node.click()
    node.focus()
    enumHumanInput(node, '123456qq')

    node = getNodeByAttr(nodesInput, 'id', 'password_again')
    node.click()
    node.focus()
    enumHumanInput(node, '123456qq')

    nodesA = getSubNodesByTag(body, "a")
    node = getNodeByAttr(nodesA, 'id', 'birthday_type_value')
    node.click()
    node.focus()
    ie6.waitBusy()
    ie6.waitReadyState()
    nodesLi = getSubNodesByTag(body, "li")
    node = getNodeByAttr(nodesLi, 'id', 'birthday_0')
    node.click()
    ie6.waitBusy()
    ie6.waitReadyState()


    node = getNodeByAttr(nodesInput, 'id', 'year_value')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    ie6.waitBusy()
    ie6.waitReadyState()
    node = getNodeByAttr(nodesLi, 'id', 'year_0')
    node.click()
    time.sleep(humanInterval)
    ie6.waitBusy()
    ie6.waitReadyState()
    
    node = getNodeByAttr(nodesInput, 'id', 'month_value')
    node.click()
    node.focus()
    ie6.waitBusy()
    ie6.waitReadyState()
    node = getNodeByAttr(nodesLi, 'id', 'month_0')
    if node != None:
        node.click()
        time.sleep(humanInterval)
        ie6.waitBusy()
        ie6.waitReadyState()

    node = getNodeByAttr(nodesInput, 'id', 'day_value')
    node.click()
    node.focus()
    ie6.waitBusy()
    ie6.waitReadyState()
    node = getNodeByAttr(nodesLi, 'id', 'day_0')
    if node != None:
        node.click()
        time.sleep(humanInterval)
        ie6.waitBusy()
        ie6.waitReadyState()

    node = getNodeByAttr(nodesInput, 'id', 'code')
    if node!=None:
        codeStr = get_code_str(ie6, imgVerifior);
        node.click()
        node.focus()
        enumHumanInput(node, codeStr)
        ie6.waitBusy()
        ie6.waitReadyState()

    oldURL = ie6.locationURL()
    node = getNodeByAttr(nodesInput, 'id', 'submit')
    node.click()


    ie6.waitBusy()
    ie6.waitNavigate(oldURL)

    if ie6.locationURL()==oldURL:
        imgVerifior.reportError()
        return False

    return True

def view_a_shop(shopIE):
##    body = shopIE.getBody()
##    nodesImg = getSubNodesByTag(body, "img")
##    allPossibleNode = []
##    for node in nodesImg:
##        nodeParent = node.parentElement
##        if nodeParent!=None:
##            if nodeParent.tagName==u"a" or nodeParent.tagName==u"A":
##                href = nodeParent.getAttribute("href")
##                if type(href)==unicode and href!=u"":
##                    if u"detail" in href:
##                        allPossibleNode += [nodeParent]
##
##    for node in allPossibleNode:
##        print node

    window = shopIE.getWindow()
    for i in range(15):
        window.scrollBy(0,15)
        time.sleep(0.2)
    window.moveTo(window.screenLeft-100, window.screenTop-100)

    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


if __name__=='__main__':
    url = "http://hyxjf.tmall.com/?spm=a220o.1000855.w3-17818260047.2.zjWNtO&scene=taobao_shop&scene=taobao_shop"
    
    ieExplorer = IEExplorer()
    ieExplorer.openURL(url)
    print ieExplorer.getIE()
    ieExplorer.setVisible(1)
    ieExplorer.waitBusy()
    ieExplorer.waitReadyState()
    view_a_shop(ieExplorer)
