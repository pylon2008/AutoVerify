# coding=GBK
import sys
sys.path.append('C:\Python27\Lib\site-packages\pytesser')

import win32com.client, win32inet, win32file
import time, os
import Image,ImageEnhance,ImageFilter
from pytesser import *
from verfcoderecognizer import *

def set_element_value(ie, elementID, value):
    thisValue = ''
    for c in value:
        thisValue = thisValue + c
        ie.Document.getElementById(elementID).value = thisValue
        time.sleep(0.2)
    return thisValue

def set_node_value(node, value):
    thisValue = ''
    for c in value:
        thisValue = thisValue + c
        node.value = thisValue
        time.sleep(0.2)
    return thisValue

def exist_ie(url):  
    ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'  
    ies=win32com.client.DispatchEx(ShellWindowsCLSID)  
    if len(ies)==0:  
        return None  
    for ie in ies:  
        if ie.LocationURL==url:  
            return ie  
    return None

def new_ie(url):  
    ie=win32com.client.Dispatch("InternetExplorer.Application")  
    ie.Navigate(url)  
    return ie  


def open_ie(url):  
    """ 
    >>> myie = ie.NewIE() 
    """  
    ie=exist_ie(url)  
    if ie==None:  
        ie=new_ie(url)  
    return ie  

def wait_ie(ie):  
    while ie.Busy:  
        time.sleep(1)  

def visible(ie):  
    ie.Visible=1-ie.Visible  

def get_body(ie):  
    wait_ie(ie)  
    return ie.Document.body  

def get_nodes(parentNode,tag):  
    """ 
    >>> coldiv=GetNodes(body,"div") 
    """  
    childNodes=[]  
    for childNode in parentNode.getElementsByTagName(tag):  
        childNodes.append(childNode)  
    return childNodes  

def get_node_by_attr(Nodes,nodeattr,nodeval):  
    """ 
    >>> div_id_editor=NodeByAttr(coldiv,"id","editor_ifr") 
    """  
    for node in Nodes:  
        if str(node.getAttribute(nodeattr))==nodeval:  
            return node  
    return None  

def get_code_str_from_image(image_name, imgVerifior):
    return imgVerifior.getCodeFromImagePath(image_name, 3004)


def get_code_str(ie6, imgVerifior):
    body = get_body(ie6)
    nodesImg = get_nodes(body, "img")  
    codeImgElement = get_node_by_attr(nodesImg, 'id', 'code_img')
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

def get_qq_num(ie6, imgVerifior):
    humanInterval = 0.2

    body = get_body(ie6)
    nodesInput = get_nodes(body, "input")

    
    node = get_node_by_attr(nodesInput, 'id', 'nick')
    node.click()
    node.focus()
    set_node_value(node, 'pylon2888')

    node = get_node_by_attr(nodesInput, 'id', 'password')
    node.click()
    node.focus()
    set_node_value(node, '123456qq')

    node = get_node_by_attr(nodesInput, 'id', 'password_again')
    node.click()
    node.focus()
    set_node_value(node, '123456qq')

    nodesA = get_nodes(body, "a")
    node = get_node_by_attr(nodesA, 'id', 'birthday_type_value')
    node.click()
    node.focus()
    nodesLi = get_nodes(body, "li")
    node = get_node_by_attr(nodesLi, 'id', 'birthday_0')
    node.click()
    node.focus()
    wait_ie(ie6)

    node = get_node_by_attr(nodesInput, 'id', 'year_value')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    wait_ie(ie6)
    node = get_node_by_attr(nodesLi, 'id', 'year_0')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    wait_ie(ie6)
    
    node = get_node_by_attr(nodesInput, 'id', 'month_value')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    wait_ie(ie6)
    node = get_node_by_attr(nodesLi, 'id', 'month_0')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    wait_ie(ie6)

    node = get_node_by_attr(nodesInput, 'id', 'day_value')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    wait_ie(ie6)
    node = get_node_by_attr(nodesLi, 'id', 'day_0')
    node.click()
    node.focus()
    time.sleep(humanInterval)
    wait_ie(ie6)

    node = get_node_by_attr(nodesInput, 'id', 'code')
    if node!=None:
        codeStr = get_code_str(ie6, imgVerifior);
        node.click()
        node.focus()
        set_node_value(node, codeStr)
        time.sleep(humanInterval)



    node = get_node_by_attr(nodesInput, 'id', 'submit')
    node.click()

    time.sleep(humanInterval)
    print 'after click'

    while ie6.Busy:
        print 'busy'
        time.sleep(1)
    print 'after wait'

    if ie6.LocationURL!="http://zc.qq.com/chs/decimal_ok.html":
        imgVerifior.reportError()

    print ie6.LocationURL



if __name__=='__main__':
    ie6 = open_ie("http://zc.qq.com/chs/index.html")
    print ie6
         
    ie6.Visible=1    
    wait_ie(ie6)

    imgVerifior = VerificationCodeRecognizer("", "")
    imgVerifior.login()
    
    get_qq_num(ie6, imgVerifior)
