# coding=GBK
import win32com.client, win32inet, win32file
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
    for node in Nodes:  
        if str(node.getAttribute(nodeattr))==nodeval:  
            return node  
    return None  

def get_code_str(ie6):
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
    else:
        code = 'aaaa'
    print code

    return code

def get_qq_num(ie6):
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

    codeStr = get_code_str(ie6);
    node = get_node_by_attr(nodesInput, 'id', 'code')
    node.click()
    node.focus()
    set_node_value(node, codeStr)
    time.sleep(humanInterval)



    node = get_node_by_attr(nodesInput, 'id', 'submit')
    node.click()
##    node.focus()
##    document.getElementById("submit").click()
    #IE調用
    #以上document就是頁面打開後面DOM對象，因爲頁面裏的javascript方法是在window命名空間,
    #所以如果要調用js, 可以用 document.parentWindow.doSomeThing(); 這樣來調用.
    #bbb = document.forms[1].submit()
    #print 'bbb: ', bbb
    #aaa = document.parentWindow.index.submit()
    #print 'aaa: ', aaa
    #print "num form: ", len(document.forms)
##    help(document.forms[1])
##    print 'type(document.forms[0]): ', type(document.forms[0])
##    print 'type(document.forms[1]): ', type(document.forms[1])
    time.sleep(humanInterval)
    print 'after click'

    while ie6.Busy:
        print 'busy'
        time.sleep(1)
    print 'after wait'


##    while 1:    
##        state = ie6.ReadyState    
##        print state
##        print ie6.LocationURL
##        if state == 4:
##            break
####        if state ==4 and str(ie.LocationURL) == "http://home.cnblogs.com/":    
####            break
##        time.sleep(1)
    #print "登陆成功" 
    #print "你的昵称是："




if __name__=='__main__':
    ie6 = open_ie("http://zc.qq.com/chs/index.html")
    print ie6
         
    ie6.Visible=1    
    wait_ie(ie6)

    get_qq_num(ie6)
