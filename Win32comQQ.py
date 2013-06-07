# coding=GBK
import win32com.client, win32inet, win32file
import time, os

def get_qq_num():
    ie6=win32com.client.Dispatch("InternetExplorer.Application")
    print ie6
    ie6.Navigate("http://zc.qq.com/chs/index.html")     
    ie6.Visible=1    
    while ie6.Busy:     
        time.sleep(1)

    return
        
    document=ie6.Document
    document.getElementById("nick").click()
    time.sleep(0.2)
    document.getElementById("nick").value="pylon2888"
    time.sleep(0.2)
    
    document.getElementById("password").click()
    time.sleep(0.2)
    document.getElementById("password").value="123456qq"
    time.sleep(0.2)

    document.getElementById("password_again").click()
    time.sleep(0.2)
    document.getElementById("password_again").value="123456qq"
    time.sleep(0.2)

    document.getElementById("birthday_type_value").click()
    time.sleep(0.2)
    document.getElementById("birthday_0").click()
    time.sleep(0.2)
    document.getElementById("year_value").click()
    time.sleep(0.2)
    document.getElementById("year_0").click()
    time.sleep(0.5)
    document.getElementById("month_value").click()
    time.sleep(0.2)
    document.getElementById("month_0").click()
    time.sleep(0.5)
    document.getElementById("day_value").click()
    time.sleep(0.2)
    document.getElementById("day_0").click()
    time.sleep(0.5)

    document.getElementById("code").click()
    time.sleep(0.2)
    document.getElementById("code").value = 'saas'
    time.sleep(0.2)

    codeImgElement = document.getElementById("code_img")
    time.sleep(0.2)
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

    print 'before click'
    time.sleep(0.2)
    document.getElementById("submit").click()
    time.sleep(0.2)
    print 'after click'

    while 1:    
        state = ie6.ReadyState    
        print state
        if state == 4:
            break
##        if state ==4 and str(ie.LocationURL) == "http://home.cnblogs.com/":    
##            break
        sleep(1)
    print "登陆成功" 
    print "你的昵称是："




if __name__=='__main__':
    get_qq_num()
