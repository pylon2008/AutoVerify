#coding=GBK
import urllib2
import win32api, win32inet
import win32con



def setIERefresh():
    INTERNET_OPTION_REFRESH = 0x000025
    INTERNET_OPTION_SETTINGS_CHANGED = 0x000027
    cc = win32inet.InternetSetOption(None, INTERNET_OPTION_SETTINGS_CHANGED, None)
    cc = win32inet.InternetSetOption(None, INTERNET_OPTION_REFRESH, None)

def setProxy(proxy):
    pathInReg='Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
    key=win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,pathInReg,0,win32con.KEY_ALL_ACCESS)

    value,enableType = win32api.RegQueryValueEx(key,'ProxyEnable')
    if value==0:
        win32api.RegSetValueEx(key,'ProxyEnable',0,win32con.REG_DWORD,1)

    d = win32api.RegSetValueEx(key,'ProxyServer',0,win32con.REG_SZ,proxy)
    c = win32api.RegQueryValueEx(key,'ProxyServer')
    win32api.RegCloseKey(key)
    setIERefresh()

def clearProxy():
    pathInReg='Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
    key=win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,pathInReg,0,win32con.KEY_ALL_ACCESS)
    value,enableType = win32api.RegQueryValueEx(key,'ProxyEnable')
    if value==1:
        win32api.RegSetValueEx(key,'ProxyEnable',0,win32con.REG_DWORD,0)
    d = win32api.RegSetValueEx(key,'ProxyServer',0,win32con.REG_SZ,"")
    win32api.RegCloseKey(key)
    setIERefresh()
    
##    # 使用自己的代理地址，注意ProxyHandler()的参数必须是字典类型
##    # build_opener()创建一个实例句柄
##    # 使用这个句柄通过open方法访问目标网址
##    # 为了便于知道哪些代理地址不能用，这里我抛出了两个已知异常，并输出异常代理地址
##    # 最后打印出发生异常的个数
def isProxyValid(proxy):
    isOk = True
    try:
        proxy_handler = urllib2.ProxyHandler({'http':'http://'+proxy})
        opener = urllib2.build_opener(proxy_handler)
        opener.open('http://www.ip138.com/')
    except urllib2.URLError:
        print 'URLError! The bad proxy is %s' % proxy      
        isOk = False
    except urllib2.HTTPError:
        print 'HTTPError! The bad proxy is %s' % proxy
        isOk = False
    except:
        print 'Unknown Errors! The bad proxy is %s' % proxy
        isOk = False
    return isOk

def scan_proxy():
    # 用来记录发生错误的个数
    num_Error=0
    # 用来存放代理地址的文件
    f=file('proxy.txt','r')
    # 读取文件每一行的代理地址
    while True:
        line=f.readline()
        if len(line)==0:
            break
        isOk = isProxyValid(line)
        if isOk == True:
            print line
##            setProxy(line)
##            clearProxy()
##            break
        else:
            num_Error=num_Error+1
    f.close()
    print '%d Errors' % num_Error

if __name__=='__main__':
    scan_proxy()
