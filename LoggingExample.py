# coding=GBK
import logging
import logging.handlers
import poplib   
import email
import smtplib 
from email.mime.text import MIMEText 
from email.header import Header      

def multiHandle():
    logger = logging.getLogger("simple_example")
    logger.setLevel(logging.DEBUG)
    
    # create file handler which logs even debug messages
    fh = logging.FileHandler("spam.log")
    fh.setLevel(logging.DEBUG)
    
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    # "application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

def emailHandle():
    logger = logging.getLogger("simple_example")
    logger.setLevel(logging.DEBUG)
    
    # create file handler which logs even debug messages
    fh = logging.FileHandler("spam.log")
    fh.setLevel(logging.DEBUG)
    
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create email handle
    mailhost = ("smtp.sina.com", 25)
    efrom = ""
    eto = [""]
    epwd = ""
    eh = logging.handlers.SMTPHandler(mailhost, \
                                      efrom, \
                                      eto, \
                                      'Error found!', \
                                      (efrom, epwd))
    eh.setLevel(logging.CRITICAL)

    
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    eh.setFormatter(formatter)
    
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.addHandler(eh)
    
    # "application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    
def initLogging():
    LOG_FILENAME="logging.log"
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')
    curTime = datetime.datetime.now
    strTime = str(curTime)
    logging.debug("===============================================Begin Log===============================================")


def sendMail():
    sender = '' 
    receiver = '' 
    subject = 'python email test' 
    smtpserver = 'smtp.sina.com' 
    username = '' 
    password = '' 
    
    msg = MIMEText('你好','plain','utf-8')#中文需参数‘utf-8’，单字节字符不需要 
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
     
    smtp = smtplib.SMTP() 
    smtp.connect('smtp.sina.com') 
    smtp.login(username, password) 
    smtp.sendmail(sender, receiver, msg.as_string()) 
    smtp.quit()


def showmessage(mail):
    #print mail
    if mail.is_multipart():
        for part in mail.get_payload():
            showmessage(part)
    else:
        type=mail.get_content_charset()
        print "type: ", type
        print "mail.get_content_maintype(): ", mail.get_content_maintype()
        if type==None:
            print mail.get_payload()
        else:
            try:
                payload = mail.get_payload(decode = True)
                if isinstance(payload, basestring):
                    print "payload: ", payload
            except UnicodeDecodeError:
                print mail

def receMail():
    host = 'pop.sina.cn'  
    username = '@sina.cn'  
    password = ''  
      
    pop_conn = poplib.POP3(host)   
    pop_conn.user(username)   
    pop_conn.pass_(password)   

    mailCount,size=pop_conn.stat()
    #Get messages from server:
    messages = []
    for i in range(1, mailCount+1):
        msg = pop_conn.retr(i)
        messages.append( msg )

    for msg in messages:
        allMsg = '\n'.join(msg[1])
        mail = email.message_from_string(allMsg)
        print "mail================================="
        subject = email.Header.decode_header(mail['subject'])[0][0]
        subcode = email.Header.decode_header(mail['subject'])[0][1]
        subStr = subject
        if subcode != None:
            subStr = unicode(subject,subcode)
        print "Subject: ", subStr
        print "Content-Transfer-Encoding: ", mail['Content-Transfer-Encoding']
        showmessage(mail)

    pop_conn.quit()




if __name__=='__main__':
##    initLogging()
##    multiHandle()
##    emailHandle()
##    sendMail()
    receMail()
