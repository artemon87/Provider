import logging

def loggingInfo(message, fileName, section):
    logFile = 'app.log'
    FORMAT = "%(asctime)-15s %(args2)s %(args3)-8s %(message)s"
    logging.basicConfig(filename=logFile,level=logging.DEBUG, format=FORMAT)
    d = {'args2': fileName, 'args3': section}
    logging.info(message, extra=d)

def loggingWarning(message, fileName, section):
    logFile = 'app.log'
    FORMAT = "%(asctime)-15s %(args2)s %(args3)-8s %(message)s"
    logging.basicConfig(filename=logFile,level=logging.DEBUG, format=FORMAT)
    d = {'args2': fileName, 'args3': section}
    logging.warning(message, extra=d)

def loggingDebug(message, fileName, section):
    logFile = 'app.log'
    FORMAT = "%(asctime)-15s %(args2)s %(args3)-8s %(message)s"
    logging.basicConfig(filename=logFile,level=logging.DEBUG, format=FORMAT)
    d = {'args2': fileName, 'args3': section}
    logging.debug(message, extra=d)

    
