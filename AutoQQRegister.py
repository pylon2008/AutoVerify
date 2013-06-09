# Generated by the windmill services transformer
from windmill.authoring import WindmillTestClient
from bs4 import BeautifulSoup
import win32com.client,win32inet,os

def get_code_info(client):
    response = client.commands.getPageText()
    soup = BeautifulSoup(response['result'])

    fff = open('te.txt', 'w+')
    fff.write( str(response) )
    fff.close()

    codeImgUrl = soup.find(id='code_img')['src']
    print codeImgUrl
    print 'type(codeImgUrl): ', type(codeImgUrl)

    #asciiUrl = codeImgUrl.encode('ascii','ignore')
    asciiUrl = codeImgUrl.encode('gbk','ignore')
    print 'asciiUrl:', asciiUrl
    print 'type(asciiUrl): ', type(asciiUrl)
    
    code = 'bbbb'
##    acachInfo=win32inet.GetUrlCacheEntryInfo(asciiUrl)
##    if cachInfo:
##        pathSrc=cachInfo['LocalFileName']
##        print 'pathSrc:', pathSrc
##        srcPathInfo = pathSrc.split('\\')
##        srcName = srcPathInfo[-1]
##        print 'srcName:', srcName
##        pathinfo=codeImgUrl.split('/')
##        filename=pathinfo[-1]
##        if filename[-4:-1] != srcName[-4:-1]:
##            filename = srcName
##        pathDest = os.path.join(self.__dir,filename)
##        if os.path.isfile(pathDest): 
##            os.remove(pathDest)
##        win32file.CopyFile(pathSrc,pathDest,True)
##    else:
##        code = 'aaaa'

    return code


    
def setup_module(module):
    client = WindmillTestClient(__name__)

    client.open(url=u'http://zc.qq.com/')
    client.waits.forPageLoad(timeout=10)
    client.waits.forElement(xpath=u"//img[@id='code_img']",timeout=10)
    
    client.click(xpath=u"//input[@id='nick']")
    client.type(xpath=u"//input[@id='nick']", text=u'pylon2888')
    client.click(xpath=u"//input[@id='password']")
    client.type(xpath=u"//input[@id='password']", text=u'123456qq')
    client.click(xpath=u"//input[@id='password_again']")
    client.type(xpath=u"//input[@id='password_again']", text=u'123456qq')
    client.click(xpath=u"//a[@id='sex_1']")



    client.click(xpath=u"//a[@id='birthday_type_value']")
    client.click(xpath=u"//li[@id='birthday_0']")

    client.click(xpath=u"//input[@id='year_value']")
    #year_0 ~99
    #client.click(xpath=u"//li[@id='birthday_0']")

    client.click(xpath=u"//input[@id='month_value']")
    #month_0 ~11(1-12)
    #client.click(xpath=u"//li[@id='birthday_0']")
    
    client.click(xpath=u"//input[@id='day_value']")
    #day_0 ~30 (1-31)
    #client.click(xpath=u"//li[@id='birthday_0']")


    #code = get_code_info(client)
    code = 'aaaa'
    client.click(xpath=u"//input[@id='code']")
    client.type(xpath=u"//input[@id='code']", text=code)
    client.click(xpath=u"//input[@id='submit']")
