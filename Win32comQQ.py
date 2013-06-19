# coding=GBK
import time, os, win32inet, win32file
from verfcoderecognizer import *
from IEExplorer import *


def get_code_str_from_image(image_name, imgVerifior):
    return imgVerifior.getCodeFromImagePath(image_name, 3004)

def get_code_str(ie6, imgVerifior):
    body = ie6.getBody()
    nodesImg = getSubNodesByTag(body, "img")  
    codeImgElement = getNodeByAttr(nodesImg, 'id', 'code_img')
    codeUrl = codeImgElement.__getattr__('src')
    cachInfo=win32inet.GetUrlCacheEntryInfo(codeUrl)
    code = 'bbbb'
    if cachInfo:
        pathSrc=cachInfo['LocalFileName']
        print 'pathSrc:', pathSrc
        srcPathInfo = pathSrc.split('\\')
        srcName = srcPathInfo[-1]
        print 'srcName:', srcName
        pathinfo=codeUrl.split('/')
        filename=pathinfo[-1]
        if filename[-4:-1] != srcName[-4:-1]:
            filename = srcName
        pathDest = os.path.join('c:\\temp\\',filename)
        if os.path.isfile(pathDest): 
            os.remove(pathDest)
        win32file.CopyFile(pathSrc,pathDest,True)
        code = get_code_str_from_image(pathDest, imgVerifior)
    else:
        code = 'aaaa'
    print code

    return code

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

def get_qq_num(ieExplorer):
    a = 0
    
def reg_a_qq(ieExplorer, imgVerifior):
    isInput = input_qq_info(ieExplorer, imgVerifior)
    print isInput
    qqInfo = None
    if isInput == True:
        qqInfo = get_qq_num(ieExplorer)
    return qqInfo

if __name__=='__main__':
    url = "http://zc.qq.com/chs/index.html"
    ieExplorer = IEExplorer()
    ieExplorer.openURL(url)
    print ieExplorer.getIE()
    ieExplorer.setVisible(1)
    ieExplorer.waitBusy()
    ieExplorer.waitReadyState()

    imgVerifior = VerificationCodeRecognizer("", "")
    imgVerifior.login()

    reg_a_qq(ieExplorer, imgVerifior)
