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

def get_qq_num(ie6):
    humanInterval = 0.2

    document=ie6.Document
    document.getElementById("nick_bg").click()
    time.sleep(humanInterval)
    document.getElementById("nick").value="pylon2888"
    
    document.getElementById("password").click()
    document.getElementById("password").focus()
    set_element_value(ie6, 'password', '123456qq')

    document.getElementById("password_again").click()
    document.getElementById("password_again").focus()
    time.sleep(humanInterval)
    set_element_value(ie6, 'password_again', '123456qq')

    document.getElementById("birthday_type_value").click()
    document.getElementById("birthday_0").click()
    document.getElementById("year_value").click()
    time.sleep(humanInterval)
    document.getElementById("year_0").click()
    time.sleep(humanInterval)
    document.getElementById("month_value").click()
    time.sleep(humanInterval)
    document.getElementById("month_0").click()
    time.sleep(humanInterval)
    document.getElementById("day_value").click()
    time.sleep(humanInterval)
    document.getElementById("day_0").click()
    time.sleep(humanInterval)

    document.getElementById("code").click()
    document.getElementById("code").focus()
    set_element_value(ie6, 'code', 'ased')
    time.sleep(humanInterval)

##    codeImgElement = document.getElementById("code_img")
##    time.sleep(humanInterval)
##    codeUrl = codeImgElement.__getattr__('src')
##    cachInfo=win32inet.GetUrlCacheEntryInfo(codeUrl)
##    code = 'bbbb'
##    if cachInfo:
##        pathSrc=cachInfo['LocalFileName']
##        print 'pathSrc:', pathSrc
##        srcPathInfo = pathSrc.split('\\')
##        srcName = srcPathInfo[-1]
##        print 'srcName:', srcName
##        pathinfo=codeUrl.split('/')
##        filename=pathinfo[-1]
##        if filename[-4:-1] != srcName[-4:-1]:
##            filename = srcName
##        pathDest = os.path.join('c:\\temp\\',filename)
##        if os.path.isfile(pathDest): 
##            os.remove(pathDest)
##        win32file.CopyFile(pathSrc,pathDest,True)
##    else:
##        code = 'aaaa'
##    print code
##
##    print 'before click'
##    time.sleep(humanInterval)
##    document.getElementById("submit").click()
##    document.forms[1].elements[1].value = 'asdf'
##    time.sleep(1)
##    set_element_value(ie6, 'code', 'ased')
##    time.sleep(1)
    document.getElementById("submit").click()
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
    ie6=win32com.client.Dispatch("InternetExplorer.Application")
    print ie6
    ie6.Navigate("http://zc.qq.com/chs/index.html")     
    ie6.Visible=1    
    while ie6.Busy:     
        time.sleep(1)

    get_qq_num(ie6)
