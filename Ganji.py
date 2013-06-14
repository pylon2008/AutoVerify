# coding=GBK

import win32com.client
import time, os

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
    idx = 0
    for node in Nodes:
        if str(node.getAttribute(nodeattr))==nodeval:  
            return node  
    return None  

def get_node_by_class_name(nodes, className):
    for node in nodes:
        if node.className==className:
            return node
    return None

    
def get_next_page_node(ie6):
    body = get_body(ie6)
    nodesA = get_nodes(body, "a")
    for node in nodesA:
        url = node.getAttribute("href")
        if (u"fang1/o" in url) and (node.className==u"next"):
            attrHref = node.getAttribute("href")
            if attrHref!=None and node.childNodes.length==1:
                childNode = node.childNodes[0]
                if childNode!=None:
                    if childNode.getAdjacentText("afterBegin")==u"��һҳ" and \
                       childNode.getAdjacentText("beforeEnd")==u"��һҳ":
                        return node
    return None

def get_list_parent_node(ie6):
    body = get_body(ie6)
    nodesDiv = get_nodes(body, "div")
    for node in nodesDiv:
        if node.className == u"listBox list-nomig-style1":
            return node
    return None

class fangInfo(object):
    def __init__(self):
        self.title = ""
        self.price = ""
        self.area = ""
        self.houseInfo = ""
        self.xiaoqu = ""
        self.quyu = ""
        self.addr = ""
        self.contactor = ""
        self.phone = ""

    def set_title(self, title):
        self.title = title

    def set_price(self, price):
        self.price = price

    def set_area(self, area):
        self.area = area

    def set_house_info(self, info):
        self.houseInfo = info

    def set_floor(self, floor):
        self.floor = floor

    def set_xiaoqu(self, xiaoqu):
        self.xiaoqu = xiaoqu

    def set_quyu(self, quyu):
        self.quyu = quyu

    def set_addr(self, addr):
        self.addr = addr

    def set_contactor(self, contactor):
        self.contactor = contactor

    def set_phone(self, phone):
        self.phone = phone
    
    def __str__(self):
        strInfo = u''
        strInfo = strInfo \
                  + u"Title: " + self.title + u"\r\n" \
                  + u"���۸�: " + self.price + u"\r\n" \
                  + u"�������: " + self.area + u"\r\n" \
                  + u"���ݸſ�: " + self.houseInfo + u"\r\n" \
                  + u"����¥��: " + self.floor + u"\r\n" \
                  + u"С������: " + self.xiaoqu + u"\r\n" \
                  + u"��������: " + self.quyu + u"\r\n" \
                  + u"С����ַ: " + self.addr + u"\r\n" \
                  + u"������ϵ: " + self.contactor + u"\r\n" \
                  + u"��ϵ��ʽ: " + self.phone + u"\r\n" \


                  
        strInfo = strInfo.encode('utf-8','ignore')
        return strInfo
               
def get_detail_info(ieSub, url):
    fang = fangInfo()
    #url = "http://nn.ganji.com/fang1/510230220x.htm"
    ie = open_ie(url)
    #ie.Visible = 1   
    wait_ie(ie)
    body = get_body(ie)
    nodeWrapper = ie.Document.getElementById("wrapper")
    
    nodesDiv = get_nodes(nodeWrapper, "div")
    nodeLeft = get_node_by_class_name(nodesDiv, u"leftBox")
    nodesDiv = get_nodes(nodeLeft, "div")
    nodesHl = get_nodes(nodeLeft, "h1")
    nodesUL = get_nodes(nodeLeft, "ul")
    
    nodeTitleName = get_node_by_class_name(nodesHl, u"title-name")
    title = nodeTitleName.getAdjacentText("afterBegin")
    fang.set_title( title )
    print title
    print url

    nodeBasicInfo = get_node_by_class_name(nodesDiv, u"basic-info")
    nodeBasicInfoUl = nodeBasicInfo.childNodes[0]
    price = nodeBasicInfoUl.childNodes[0].childNodes[2].getAdjacentText("afterBegin")
    fang.set_price(price)

    area = nodeBasicInfoUl.childNodes[1].getAdjacentText("beforeEnd")
    fang.set_area(area)

    houseinfo = nodeBasicInfoUl.childNodes[2].getAdjacentText("beforeEnd")
    fang.set_house_info(houseinfo)

    floor = nodeBasicInfoUl.childNodes[3].getAdjacentText("beforeEnd")
    fang.set_floor(floor)

##    print nodeBasicInfoUl.childNodes[4].childNodes[0].getAdjacentText("beforeBegin")
##    print nodeBasicInfoUl.childNodes[4].childNodes[0].getAdjacentText("afterBegin")
##    print nodeBasicInfoUl.childNodes[4].childNodes[0].getAdjacentText("beforeEnd")
##    print nodeBasicInfoUl.childNodes[4].childNodes[0].getAdjacentText("afterEnd")
##
##    print nodeBasicInfoUl.childNodes[4].childNodes[2].getAdjacentText("beforeBegin")
##    print nodeBasicInfoUl.childNodes[4].childNodes[2].getAdjacentText("afterBegin")
##    print nodeBasicInfoUl.childNodes[4].childNodes[2].getAdjacentText("beforeEnd")
##    print nodeBasicInfoUl.childNodes[4].childNodes[2].getAdjacentText("afterEnd")

    if nodeBasicInfoUl.childNodes[4].childNodes.length > 2:
        xiaoqu = nodeBasicInfoUl.childNodes[4].childNodes[2].getAdjacentText("afterBegin")
    else:
        xiaoqu = nodeBasicInfoUl.childNodes[4].getAdjacentText("beforeEnd")
    fang.set_xiaoqu(xiaoqu)

    quyu = nodeBasicInfoUl.childNodes[5].childNodes[2].getAdjacentText("afterBegin") \
           + "-" \
           + nodeBasicInfoUl.childNodes[5].childNodes[4].getAdjacentText("afterBegin") \
           + "-" \
           + nodeBasicInfoUl.childNodes[5].childNodes[6].getAdjacentText("afterBegin")
    fang.set_quyu(quyu)

    addr = nodeBasicInfoUl.childNodes[6].childNodes[2].getAdjacentText("afterBegin")
    fang.set_addr(addr)

    nodeBasicInfoContact = nodeBasicInfo.childNodes[1]
    contactor = nodeBasicInfoContact.childNodes[0].childNodes[0].childNodes[1].getAdjacentText("afterBegin") \
               + "-" \
               + nodeBasicInfoContact.childNodes[0].childNodes[0].childNodes[3].getAdjacentText("afterBegin")
    fang.set_contactor(contactor)

    phone = nodeBasicInfoContact.childNodes[1].childNodes[2].childNodes[0].getAdjacentText("afterBegin")
    fang.set_phone(phone)

    ie.Quit()
    #print fang
    return fang

def get_info(ieSub, rootNode):
    nodesA = get_nodes(rootNode, "a")
    infoSet = []
    for node in nodesA:
        if node.className==u"list-title":
            newUrl = node.getAttribute("href")
            info = get_detail_info(ieSub, newUrl)
            infoSet.append(info)
    return infoSet
             
    
def get_fang_info(ieMain, ieSub):
    node = get_next_page_node(ieMain)
    nodeListParent = get_list_parent_node(ieMain)
    nodesInfoSet = get_nodes(nodeListParent, "dl")
    infoSet = []
    for infoNode in nodesInfoSet:
        infoSet = infoSet + get_info(ieSub, infoNode)
        #break

    print 'һ��',len(infoSet),'����Ϣ.'
    idx = 0
    for info in infoSet:
        print '��', idx, '��'
        print info
        idx += 1


if __name__=='__main__':
    ieMain = open_ie("http://nn.ganji.com/fang1/")
    ieMain.Visible=1    
    wait_ie(ieMain)

    ieSub = None
##    ieSub = open_ie("http://www.baidu.com")
##    ieSub.Visible=1    
##    wait_ie(ieSub)
         

    get_fang_info(ieMain, ieSub)


##    ie6.Quit()
