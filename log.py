import logging

def loggingInfo(message, fileName, section):
    try:
        logFile = 'app.log'
        FORMAT = "%(asctime)-15s %(args2)s %(args3)-8s %(message)s"
        logging.basicConfig(filename=logFile,level=logging.DEBUG, format=FORMAT)
        d = {'args2': fileName, 'args3': section}
    except Exception as e:
        print(e)
    logging.info(message, extra=d)

def loggingWarning(message, fileName, section):
    try:
        logFile = 'app.log'
        FORMAT = "%(asctime)-15s %(args2)s %(args3)-8s %(message)s"
        logging.basicConfig(filename=logFile,level=logging.DEBUG, format=FORMAT)
        d = {'args2': fileName, 'args3': section}
    except Exception as e:
        print(e)
    logging.warning(message, extra=d)

def loggingDebug(message, fileName, section):
    try:
        logFile = 'app.log'
        FORMAT = "%(asctime)-15s %(args2)s %(args3)-8s %(message)s"
        logging.basicConfig(filename=logFile,level=logging.DEBUG, format=FORMAT)
        d = {'args2': fileName, 'args3': section}
    except Exception as e:
        print(e)
    logging.debug(message, extra=d)

    
