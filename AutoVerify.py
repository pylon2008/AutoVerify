# coding=utf-8
import urllib,urllib2,httplib,cookielib

def auto_login_hi(url,name,pwd):
    url_hi="http://passport.baidu.com/?login"
    
    #设置cookie
    cookie=cookielib.CookieJar()
    cj=urllib2.HTTPCookieProcessor(cookie)
    
    #设置登录参数
    postdata=urllib.urlencode({'username':name,'password':pwd})
    
    #生成请求
    request=urllib2.Request(url_hi,postdata)
    print request
    
    #登录百度
    opener=urllib2.build_opener(request,cj)
    f=opener.open(request)
    print f
    
    #打开百度HI空间页面
    hi_html=opener.open(url)
    return hi_html

##if __name__=='__main__':
##    name='pyliang_2008'
##    password='2008pylpyl'
##    url='http://hi.baidu.com/cdkey51'#例如：url='http://hi.baidu.com/cdkey51'
##    
##    h=auto_login_hi(url,name,password)
##    print h.read()#h里面的内容便是登录后的页面内容


##url = 'http://passport.baidu.com/?login'      #要尝试的url,还是把url改下吧
##values = {'username' : 'pyliang_2008',
##                'password' : '2008pylpyl'}                   #post提交的数据
##data = urllib.urlencode(values)                  #对提交的数据进行编码
##req = urllib2.Request(url, data)                 #形成一个url请求
##response = urllib2.urlopen(req)                #发送签名的请求
##the_page = response.read()                    #读取返回的页面
##print the_page                                         #输出返回的页面




#encoding=utf-8
import sys
import re
import urllib2
import urllib
import cookielib

class Renren(object):
   
    def __init__(self):
        self.name = self.pwd = self.content = self.domain = self.origURL =  ''
        self.operate = ''#登录进去的操作对象
        self.cj=cookielib.CookieJar()
        #self.cj = cookielib.LWPCookieJar()
##        try: 
##            self.cj.revert('renren.coockie') 
##        except Exception,e:
##            print e
           
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)
   
   
    def setinfo(self,username,password,domain,origURL):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password
        self.domain = domain
        self.origURL = origURL

    def login(self):
        '''登录人人网'''
        params = {'domain':self.domain,'origURL':self.origURL,'email':self.name, 'password':self.pwd}
        print 'login.......'
        req = urllib2.Request( 
            'http://www.renren.com/PLogin.do', 
            urllib.urlencode(params) 
        )
       
        self.operate = self.opener.open(req)
        print self.operate
        print self.operate.geturl()

        if self.operate.geturl() == 'http://www.renren.com/Home.do': 
            print 'Logged on successfully!'
            self.cj.save('renren.coockie')
            self.__viewnewinfo()
        else:
            print 'Logged on error'
   
    def __viewnewinfo(self):
        '''查看好友的更新状态'''
        self.__caiinfo()
       
       
    def __caiinfo(self):
        '''采集信息'''
       
        h3patten = re.compile('<h3>(.*?)</h3>')#匹配范围
        apatten = re.compile('<a.+>(.+)</a>:')#匹配作者
        cpatten = re.compile('</a>(.+)\s')#匹配内容       
        infocontent = self.operate.readlines()
#        print infocontent 
        print 'friend newinfo:' 
        for i in infocontent:
            content = h3patten.findall(i)
            if len(content) != 0:
                for m in content:
                    username = apatten.findall(m)
                    info = cpatten.findall(m)
                    if len(username) !=0:
                        print username[0],'说:',info[0]
                        print '----------------------------------------------'
                    else:
                        continue
   
ren = Renren()
username = 'pyliang_2008@163.com'#你的人人网的帐号
password = '2008pylpyl'#你的人人网的密码
domain = 'renren.com'#人人网的地址
origURL = 'http://www.renren.com/Home.do'#人人网登录以后的地址
ren.setinfo(username,password,domain,origURL)
ren.login()
