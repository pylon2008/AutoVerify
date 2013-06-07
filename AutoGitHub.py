from windmill.authoring import WindmillTestClient
import functest
import time

##def setup_module(module):
##    client = WindmillTestClient(__name__)
##    
##    client.open(url='http://www.github.com/')
##    print 'before waits'
##    client.waits.forElement(xpath=u"//a[@class='button'][name(..)='div']",timeout=5)
##    #client.click(id=u'button')
##    #time.sleep(5)
##    print 'before click'
##    clickResult = client.click(xpath=u"//a[@class='button'][name(..)='div']")
##    print 'type(clickResult): ', type(clickResult)
##
####    email = ''
####    password = ''
####    client.type(text=email, id=u'email')
####    client.type(text=password, id=u'pass')
####    client.click(value=u"Login")
####    client.waits.forPageLoad(timeout=u'60000')


def setup_module(module):
    client = WindmillTestClient(__name__)
    
    #client.open(url='http://www.qq.com/')
    client.open(url='http://zc.qq.com/')
    client.waits.forPageLoad()

    client.click(xpath="//a[@href='http://zc.qq.com/']")
        
    client.waits.forElement(xpath="//form[@method='post']",timeout=5)

    client.type(text='', xpath="//input[@id='nick']")
    
    
    print 'before click'
    clickResult = client.click(xpath=u"//a[@class='button'][name(..)='div']")
    print 'type(clickResult): ', type(clickResult)

