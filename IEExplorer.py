# coding=GBK
import win32com.client
import time

def existIE(url):
    ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'  
    ies = win32com.client.DispatchEx(ShellWindowsCLSID)  
    if len(ies)==0:  
        return None  
    for ie in ies:  
        if ie.LocationURL==url:  
            return ie  
    return None

def enumHumanInput(node, value):
    thisValue = ''
    for c in value:
        thisValue = thisValue + c
        node.value = thisValue
        time.sleep(0.2)
    return thisValue

# 根据tag名称获取父节点的所有子节点
def getSubNodesByTag(parentNode, tag):
    childNodes=[]  
    for childNode in parentNode.getElementsByTagName(tag):  
        childNodes.append(childNode)  
    return childNodes

#在节点集合nodes中查找属性attr为值val的节点
def getNodeByAttr(nodes, attr, val):
    for node in nodes:  
        if str(node.getAttribute(attr))==val:  
            return node  
    return None

class IEExplorer(object):
    def __init__(self):
        self.ie = None
        self.oldURL = ""

    def newIE(self, url):  
        self.ie = win32com.client.Dispatch("InternetExplorer.Application")
        self.navigate(url)

    def openURL(self, url):
        self.ie = existIE(url)
        if self.ie == None:
            self.newIE(url)

    def navigate(self, url):
        self.ie.Navigate(url)

    def waitReadyState(self):
        while True:
            if self.ie.ReadyState==4:
                break
            else:
                time.sleep(0.5)
        
    def waitNavigate(self, oldURL):
        self.waitReadyState()
        timeout = 0.0
        while True:
            if self.ie.LocationURL!=oldURL or timeout>=2.0:
                break
            else:
                deltaTime = 0.5
                time.sleep(deltaTime)
                timeout += deltaTime
                
    def waitBusy(self):
        while self.isBusy():
            time.sleep(0.5)

    def setVisible(self, visible):
        self.ie.Visible = visible

    def getIE(self):
        return self.ie
    
    def getBody(self):
        return self.ie.Document.body

    def quit(self):
        self.ie.quit()

    def isBusy(self):
        return self.ie.Busy

    def locationURL(self):
        return self.ie.LocationURL



