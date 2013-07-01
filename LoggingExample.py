# coding=GBK
import logging
import logging.handlers

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
##    LOG_FILENAME="logging.log"
##    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')
##    curTime = datetime.datetime.now
##    strTime = str(curTime)
##    logging.debug("===============================================Begin Log===============================================")
    multiHandle()


if __name__=='__main__':
    #initLogging()
    emailHandle()
