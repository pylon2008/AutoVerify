from windmill.authoring import WindmillTestClient
import functest

def setup_module(module):
    client = WindmillTestClient(__name__)
    
    client.open(url='http://www.github.com/')
    print 'before waits'
##    client.waits.forElement(xpath=u"//a[@class='button'][name(..)='div'][../@class='header-actions']",timeout=30000)
    #client.click(id=u'button')
    print 'before click'
    clickResult = client.click(xpath=u"//a[@class='button'][name(..)='div']")
    print 'type(clickResult): ', type(clickResult)

##    email = ''
##    password = ''
##    client.type(text=email, id=u'email')
##    client.type(text=password, id=u'pass')
##    client.click(value=u"Login")
##    client.waits.forPageLoad(timeout=u'60000')
