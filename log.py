import logging

def loggingInfo(message):
    logFile = 'app.log'
    logging.basicConfig(filename=logFile,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    logging.info(message)

    
