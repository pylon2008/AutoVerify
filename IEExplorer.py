# coding=GBK
import win32com.client, win32gui, win32api
import time, datetime, traceback, logging

# ��ȡ��Ļ�Ŀ���
##width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
##height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

IE_INTERVAL_TIME_CLOSE = 1
IE_INTERVAL_TIME_SACROLL = 0.08
IE_TIME_OUT_SCROLL = 2
IE_TIME_OUT_NEW_PAGE = 10

def getAllRunningIE():
    ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'  
    ies = win32com.client.DispatchEx(ShellWindowsCLSID)
    copyIes = []
    for ie in ies:
        copyIes.append(ie)
    return copyIes

def closeAllRunningIE():
    try:
        ies = getAllRunningIE()
        logging.debug("len(ies): %d", len(ies))
        for ie in ies:
            logging.debug("ie.LocationURL: %s", ie.LocationURL)
            if u"http://" in ie.LocationURL:
                logging.debug("closeAllRunningIE: %s", ie.LocationURL)
                while ie.Busy==True:
                    ie.stop()
                    time.sleep(0.1)
                ie.quit()
                time.sleep(IE_INTERVAL_TIME_CLOSE)
            else:
                a = 0
    except:
        logging.error("closeAllRunningIE exception")
        traceStr = traceback.format_exc()
        logging.error(traceStr)

def existIE(url):
    ies = getAllRunningIE()
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

# ģ���˹������ı�
def enumHumanInput(node, value):
    thisValue = ''
    for c in value:
        thisValue = thisValue + c
        node.value = thisValue
        time.sleep(0.2)
    return thisValue

# ����tag���ƻ�ȡ���ڵ�������ӽڵ�
def getSubNodesByTag(parentNode, tag):
    childNodes=[]
    if parentNode != None:
        for childNode in parentNode.getElementsByTagName(tag):  
            childNodes.append(childNode)  
    return childNodes

# �ڽڵ㼯��nodes�в�������attrΪֵval�Ľڵ�
def getNodeByAttr(nodes, attr, val):
    for node in nodes:  
        if str(node.getAttribute(attr))==val:  
            return node  
    return None

# �жϽڵ��Ƿ�����Ļ��Χ��
def isNodeInScreen(node, ie):
    client = node.getBoundingClientRect()
    nodeHeight = client.bottom - client.top
    nodeMiddle = (client.bottom + client.top)/2
    clientHeight = ie.getClientHeight()
    ieMiddle = clientHeight/2
    isIn = True
    if clientHeight<=nodeHeight:
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
        self.PageTimeOut = 10.0
        self.timeBegOp = None                   # ��ʼ�������������ʱ�䣬�ӿ�ʼ������ʼ

    def newIE(self, url):  
        self.ie = win32com.client.Dispatch("InternetExplorer.Application")
        self.navigate(url)

    def openURL(self, url):
        self.ie = existIE(url)
        if self.ie == None:
            self.newIE(url)
        #self.setForeground()

    def navigate(self, url):
        self.ie.Navigate(url)

    def waitReadyState(self, totalTimeout):
        isBusy = False
        timeout = 0.0
        while True:
            if self.ie.ReadyState==4:
                break
            else:
                deltaTime = 0.5
                time.sleep(deltaTime)
                timeout += deltaTime
            if timeout>=totalTimeout:
                isBusy = True
                break
        if isBusy==True:
            logging.debug("waitReadyState: "+str(isBusy))
        return isBusy
        
    def waitNavigate(self, oldURL, totalTimeout):
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
            if timeout>=totalTimeout:
                isBusy = True
                break
        if isBusy==True:
            logging.debug("waitNavigate: "+str(isBusy))
        return isBusy
                
    def waitBusy(self, totalTimeout):
        isBusy = False
        timeout = 0.0
        while True:
            if self.isBusy():
                deltaTime = 0.5
                time.sleep(deltaTime)
                timeout += deltaTime
            else:
                break
            if timeout>=totalTimeout:
                isBusy = True
                break
        if isBusy==True:
            logging.debug("waitBusy: "+str(isBusy))
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
        while self.waitBusy(IE_TIME_OUT_SCROLL)==True:
            self.stop()
            time.sleep(0.1)
        self.ie.quit()

    def stop(self):
        self.ie.stop()

    def isBusy(self):
        return self.ie.Busy

    def locationURL(self):
        return self.ie.LocationURL

    # ��ȡ��Ļ�Ŀ��Ӹ߶�
    def getClientHeight(self):
        return self.ie.Document.documentElement.clientHeight

    def scrollToNode(self, node):
        scrollDirection = getScrollDirection(node, self)
        scrollDelta = [20,30,40,50,60,70]
        isIn = False
        while isIn==False:
            for delta in scrollDelta:
                while self.waitBusy(IE_TIME_OUT_SCROLL)==True:
                    self.stop()
                    time.sleep(0.1)
                self.waitReadyState(IE_TIME_OUT_SCROLL)
                self.getWindow().scrollBy(0,delta*scrollDirection)
                if isNodeInScreen(node, self)==True:
                    isIn = True
                    break
            time.sleep(IE_INTERVAL_TIME_SACROLL)

    def stayInSubPage(self, timeOut):
        scrollDelta = [20,30,40,50,60,70]
        a = datetime.datetime.now()
        self.timeBegOp = a
        while True:
            for delta in scrollDelta:
                while self.waitBusy(IE_TIME_OUT_SCROLL)==True:
                    self.stop()
                    time.sleep(0.1)
                isBusy = self.waitReadyState(IE_TIME_OUT_SCROLL)
                if isBusy==True:
                    logging.debug("stayInSubPage::waitReadyState: "+str(isBusy))
                self.getWindow().scrollBy(0,delta)
            time.sleep(IE_INTERVAL_TIME_SACROLL)
            b = datetime.datetime.now()
            deltaTime = (b-a).seconds
            if deltaTime >= timeOut:
                break



