# coding=GBK
import time, os, win32inet, win32file, logging
import win32api,win32gui,win32con, traceback, socket
import random
from IEExplorer import *
from IEProxy import *
from NetManager import *
import xlrd, xlwt

NUM_BAT_TAOBAO_BAOBEI_VIEW = 3                  # һ���������������
NUM_SUB_PAGE_MIN = 2                            # ��ҳ��������Сֵ
NUM_SUB_PAGE_MAX = 4                            # ��ҳ���������ֵ
TIME_PROXY_CHANGE = 30                          # �л�IP��ַ��ʱ��

class TaobaoBaobei(object):
    def __init__(self, mainIE):
        self.mainIE = mainIE
        self.subIESet = []
        self.imgHrefNodes = []
        self.subNodes = []
        self.timeBegOp = None                   # ��ʼ�������������ʱ�䣬�ӿ�ʼ������ʼ

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

    def baobeiSrcollBeg(self):
        self.timeBegOp = datetime.datetime.now()
        mainIE = self.getMainIE()
        while mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
            mainIE.stop()
            time.sleep(0.1)
        mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
        mainIE.setForeground()
        while mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
            mainIE.stop()
            time.sleep(0.1)
        isReady = mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
        time.sleep(1)
        timeOut = random.randint(3, 5)
        mainIE.stayInSubPage(timeOut)

    def openCurBaobei(self):
        logging.debug("openCurBaobei")
        self.getImgHrefNodes()
        self.getRandomSubIE()
        
        numSubIE = self.getNumSubIE()
        for subIdx in range(numSubIE):
            debugInfo = "subIdx: " + str(subIdx) + ", url: " + self.subNodes[subIdx].getAttribute("href")
            logging.debug(debugInfo)
            debugInfo = "come back to mainIE waitBusy before setForeground: "
            logging.debug(debugInfo)
            # �ر�������
            while self.mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                self.mainIE.stop()
                time.sleep(0.1)
            self.mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
            self.mainIE.setForeground()
            time.sleep(1)
            self.mainIE.resizeMax()
            time.sleep(1)
            debugInfo = "come back to mainIE waitBusy after setForeground: "
            logging.debug(debugInfo)
            while self.mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
                self.mainIE.stop()
                time.sleep(0.1)
            self.mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)

            # ����ҳ��
            logging.debug("self.mainIE.scrollToNode")
            subNode = self.subNodes[subIdx]
            self.mainIE.scrollToNode(subNode)
            subNode.focus()
            logging.debug("self.createNewSubIE")
            self.createNewSubIE(subIdx)

            # ������ҳ��
            logging.debug("subIE.stayInSubPage")
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
        self.mainIE = []                                    # �����������
        self.baobeiSet = []                                 # �����ļ������еı�������
        self.numBaobei = NUM_BAT_TAOBAO_BAOBEI_VIEW         # һ�δ򿪵ı���������

        self.readUrlConfig()

        numUnvisit = self.numAllUnvisit()
        if self.numBaobei > numUnvisit:
            self.numBaobei = numUnvisit

        if self.numBaobei<=0:
            return None

        logging.debug("numUnvisit: %d, self.numBaobei: %d", numUnvisit, self.numBaobei)
        # �����ȡ���ʶ���
        unvisitIdx = self.allUnvisitIdx()
        self.randomVisit = []
        for i in range(self.numBaobei):
            while True:
                r = random.randint(0, len(unvisitIdx)-1)
                rr = unvisitIdx[r]
                if rr not in self.randomVisit:
                    if self.baobeiSet[rr][0] > 0:
                        self.randomVisit.append(rr)
                        break
        randomStr = "self.randomVisit: " + str(self.randomVisit)
        logging.debug(randomStr)
        
    def numVisit(self):
        return len(self.randomVisit)

    def numAllUnvisit(self):
        numUnvisit = 0
        for baobei in self.baobeiSet:
            if baobei[0]>0:
                numUnvisit += 1
        return numUnvisit

    def allUnvisitIdx(self):
        unvisit = []
        for i in range(len(self.baobeiSet)):
            baobei = self.baobeiSet[i]
            if baobei[0]>0:
                unvisit.append(i)
        return unvisit

    def hasUnvisit(self):
        numUnvisit = self.numAllUnvisit()
        return numUnvisit > 0

    def createBaobei(self, visitIdx):
        realIdx = self.randomVisit[visitIdx]
        self.baobeiSet[realIdx][0] -= 1
        url = self.baobeiSet[realIdx][1]
        ieExplorer = IEExplorer()
        ieExplorer.openURL(url)
        ieExplorer.setVisible(1)
        store = TaobaoBaobei(ieExplorer)
        self.mainIE.append(store)
        debugInfo = "createBaobei visitIdx(" + str(visitIdx) + "): " + url
        logging.debug(debugInfo)

    def getBaobei(self, visitIdx):
        return self.mainIE[visitIdx]

    def readUrlConfig(self):
        # ��ȡ���б���
        try:
            filePath = "UrlConfig.xls"
            wb = xlrd.open_workbook(filePath)
            sheet = wb.sheet_by_index(0)
            for row_index in range(sheet.nrows):
                numVisit = sheet.cell(row_index,0).value
                numVisit = (int)(numVisit)
                url = sheet.cell(row_index,1).value
                self.baobeiSet.append( [numVisit,url] )
        except:
            logging.error("UrlConfig.xls read error!")
            traceStr = traceback.format_exc()
            logging.error(traceStr)
           
    def writeUrlConfig(self):
        try:
            wb = xlwt.Workbook()
            sheet = wb.add_sheet('sheet 1')
            for row_index in range(len(self.baobeiSet)):
                baobei = self.baobeiSet[row_index]
                num = baobei[0]-1
                url = baobei[1]
                sheet.write(row_index,0,num)
                sheet.write(row_index,1,url)
            sheet.col(1).width = 3333*8
            filePath = "UrlConfig_backup.xls"
            wb.save(filePath)
            win32file.DeleteFile(u"UrlConfig.xls")
            win32file.CopyFile(u"UrlConfig_backup.xls", u"UrlConfig.xls", False)
        except:
            logging.error("UrlConfig_backup.xls write error!")
            traceStr = traceback.format_exc()
            logging.error(traceStr)
       
    def closeAllIE(self):
        numVisitBaobei = self.numVisit()
        for mainIdx in range(numVisitBaobei):
            baobei = self.getBaobei(mainIdx)
            debugInfo = "mainIdx: "+ str(mainIdx) + ", type(baobei): " + str(type(baobei)) + ", baobei.getNumSubIE(): " + str(baobei.getNumSubIE())
            logging.debug(debugInfo)
            for subIdx in range(baobei.getNumSubIE()):
                subIE = baobei.getNewSubIE(subIdx)
                debugInfo = "subIdx: "+str(subIdx)+ ", type(subIE): "+ str(type(subIE))
                logging.debug(debugInfo)
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

    # ��3����������
    numVisitBaobei = viewer.numVisit()
    for idx in range(numVisitBaobei):
        viewer.createBaobei(idx)

    timeBegOp = None
    # ÿ������������й���
    for idx in range(numVisitBaobei):
        debugInfo = "baobeiSrcollBeg: " + str(idx)
        logging.debug(debugInfo)
        baobei = viewer.getBaobei(idx)
        baobei.baobeiSrcollBeg()
        if idx==0:
            timeBegOp = baobei.getTimeBegOp()
    
    # �򿪱����������ҳ�棬��������ҳ��
    for idx in range(numVisitBaobei):
        baobei = viewer.getBaobei(idx)
        mainIE = baobei.getMainIE()
        debugInfo = "mainIE waitBusy before setForeground: " + str(idx)
        logging.debug(debugInfo)
        while mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
            mainIE.stop()
            time.sleep(0.1)
        mainIE.setForeground()
        mainIE.resizeMax()
        debugInfo = "mainIE waitBusy after setForeground: " + str(idx)
        while mainIE.waitBusy(IE_TIME_OUT_NEW_PAGE)==True:
            mainIE.stop()
            time.sleep(0.1)
        mainIE.waitReadyState(IE_TIME_OUT_NEW_PAGE)
        baobei.openCurBaobei()

    # ͣ��
    timePass = (datetime.datetime.now() - timeBegOp).seconds
    timeSleep = 360 - timePass
    if timeSleep <= 45:
        timeSleep = 45
    logging.debug("timeSleep: %d", timeSleep)
    time.sleep(timeSleep)

    # �ر����б���
    viewer.closeAllIE()

    # write URL config
    viewer.writeUrlConfig()
    return viewer.hasUnvisit()

def initLogging():
    LOG_FILENAME="TaobaoViewer.log"
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')
    curTime = datetime.datetime.now
    strTime = str(curTime)
    logging.debug("===============================================Begin Log===============================================")
    logging.debug( socket.gethostname() )


def zhubajie_2897106_dowork():
    initLogging()
    netManger = None
    
    # init net manager
    try:
        netManger = NetManager()
        config = ConfigIni("Config.ini")
        netType = config.getKeyValue(u"������������")
        ethernet = config.getKeyValue(u"������������")
        user = config.getKeyValue(u"�û���")
        password = config.getKeyValue(u"����")
        netManger.setEthernetInfo(netType, ethernet, user, password)
    except:
        logging.error("��ʼ��ʧ�ܣ����������ļ���Config.ini")
        traceStr = traceback.format_exc()
        logging.error(traceStr)

    hasUnvisit = True
    batIdx = 0
    while hasUnvisit:
        logging.debug("\r\n\r\n")
        logging.debug("batIdx: %d", batIdx)

        if isOutOfData()==True:
            logging.error("isOutOfData" + str(datetime.datetime.now()))
            time.sleep(24*60*60)

        #init ev
        try:
            os.startfile("C:\\Program Files\\Internet Explorer\\iexplore.exe")
        except:
            logging.error("�հ�ҳ���쳣")
            traceStr = traceback.format_exc()
            logging.error(traceStr)

        # view baobei
        try:
            hasUnvisit = view_3_baobei()
            closeAllRunningIE()
        except:
            traceStr = traceback.format_exc()
            logging.error(traceStr)
            closeAllRunningIE()

        # change IP
        try:
            netManger.changeIP()
        except:
            traceStr = traceback.format_exc()
            logging.error(traceStr)

        # next view
        batIdx += 1


class PyResorceRelease(object):
    def __init__(self):
        a = 0

    def __del__(self):
        try:
            logging.error("release all py exe resorce")
            closeAllRunningIE()
        except:
            traceStr = traceback.format_exc()
            logging.error(traceStr)
        
def zhubajie_2897106():
    releaser = PyResorceRelease()
    zhubajie_2897106_dowork()

    
if __name__=='__main__':
    zhubajie_2897106()
