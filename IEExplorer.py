# coding=GBK
import win32com.client, win32gui, win32api
import time, datetime

# 获取屏幕的宽、高
##width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
##height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


def existIE(url):
    ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'  
    ies = win32com.client.DispatchEx(ShellWindowsCLSID)  
    if len(ies)==0:  
        return None
    for ie in ies:
        ieURL = ie.LocationURL
        if type(ie.LocationURL) == unicode:
            ieURL = ieURL.encode('GBK')
        newURL = url
        if newURL[-1]=='\n':
            newURL = newURL[0:-1]
        if type(newURL) == str:
            newURL = newURL.encode('GBK')            
        if ieURL==newURL:
            return ie
    return None

# 模拟人工输入文本
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

# 在节点集合nodes中查找属性attr为值val的节点
def getNodeByAttr(nodes, attr, val):
    for node in nodes:  
        if str(node.getAttribute(attr))==val:  
            return node  
    return None

# 判断节点是否在屏幕范围内
def isNodeInScreen(node, ie):
    client = node.getBoundingClientRect()
    nodeHeight = client.bottom - client.top
    nodeMiddle = (client.bottom + client.top)/2
    clientHeight = ie.getClientHeight()
    ieMiddle = clientHeight/2
    isIn = True
    if clientHeight<=nodeHeight:
        print clientHeight, ", ", nodeHeight
        if client.top>0 and client.top<70:
            isIn = True
        else:
            isIn = False
    else:
        dis = ieMiddle-nodeMiddle
        if dis<=50 and dis>=-50:
            isIn = True
        else:
            isIn = False
    return isIn

def getScrollDirection(node, ie):
    scrollDirection = 1
    client = node.getBoundingClientRect()
    nodeHeight = client.bottom - client.top
    nodeMiddle = (client.bottom + client.top) / 2
    clientHeight = ie.getClientHeight()
    ieMiddle = clientHeight/2
    if nodeMiddle > ieMiddle:
        scrollDirection = 1
    else:
        scrollDirection = -1
    return scrollDirection


class IEExplorer(object):
    def __init__(self):
        self.ie = None
        self.oldURL = ""
        self.PageTimeOut = 4.0

    def newIE(self, url):  
        self.ie = win32com.client.Dispatch("InternetExplorer.Application")
        self.navigate(url)

    def openURL(self, url):
        self.ie = existIE(url)
        if self.ie == None:
            self.newIE(url)
        self.setForeground()

    def navigate(self, url):
        self.ie.Navigate(url)

    def waitReadyState(self):
        isBusy = False
        timeout = 0.0
        while True:
            if self.ie.ReadyState==4:
                break
            else:
                deltaTime = 0.5
                time.sleep(deltaTime)
                timeout += deltaTime
            if timeout>=self.PageTimeOut:
                isBusy = True
                break
        return isBusy
        
    def waitNavigate(self, oldURL):
        self.waitReadyState()
        timeout = 0.0
        isBusy = False
        while True:
            if self.ie.LocationURL!=oldURL:
                break
            else:
                deltaTime = 0.5
                time.sleep(deltaTime)
                timeout += deltaTime
            if timeout>=self.PageTimeOut:
                isBusy = True
                break
        return isBusy
                
    def waitBusy(self):
        isBusy = False
        timeout = 0.0
        while True:
            if self.isBusy():
                deltaTime = 0.5
                time.sleep(deltaTime)
                timeout += deltaTime
            else:
                break
            if timeout>=self.PageTimeOut:
                isBusy = True
                break
        return isBusy

    def setVisible(self, visible):
        self.ie.Visible = visible

    def getIE(self):
        return self.ie

    def setForeground(self):
        win32gui.SetForegroundWindow(self.ie.hwnd)

    def resizeMax(self):
        WM_SYSCOMMAND = int('112', 16)
        SC_MINIMIZE = int('F020', 16)
        SC_MAXIMIZE = int('F030', 16)
        win32api.SendMessage(self.ie.hwnd, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
    
    def getBody(self):
        return self.ie.Document.body

    # window.screenLeft
    # window.screenTop
    def getWindow(self):
        return self.ie.Document.parentWindow

    def quit(self):
        self.ie.quit()

    def isBusy(self):
        return self.ie.Busy

    def locationURL(self):
        return self.ie.LocationURL

    # 获取屏幕的可视高度
    def getClientHeight(self):
        return self.ie.Document.documentElement.clientHeight

    def scrollToNode(self, node):
        scrollDirection = getScrollDirection(node, self)
        window = self.getWindow()
        scrollDelta = [20,30,40,50,60,70]
        isIn = False
        while isIn==False:
            for delta in scrollDelta:
                window.scrollBy(0,delta*scrollDirection)
                self.waitBusy()
                self.waitReadyState()
                #time.sleep(0.1)
                if isNodeInScreen(node, self)==True:
                    isIn = True
                    break
            time.sleep(0.1)

    def stayInSubPage(self, timeOut):
        window = self.getWindow()
        scrollDelta = [20,30,40,50,60,70]
        a = datetime.datetime.now()
        while True:
            for delta in scrollDelta:
                window.scrollBy(0,delta)
                self.waitBusy()
                self.waitReadyState()

            b = datetime.datetime.now()
            deltaTime = (b-a).seconds
            if deltaTime >= timeOut:
                break



