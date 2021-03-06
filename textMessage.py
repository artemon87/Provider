import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import log

class textMessage():
    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 587
        self.username = 'rubinsteinlaw.text@gmail.com'
        self.password = 'Rlo875@@@!1'
        self.to_List = []

    def fillInList(self, number):
        if number.startswith('1'):
            number = number[1:]
        ''', '@vzwpix', '@vtext.com',
               '@messaging.sprintpcs.com', '@pm.sprint.com',
               '@vmobl.com', '@mmst5.tracfone.com', '@mymetropcs.com',
               '@myboostmobile.com', '@mms.cricketwireless.net',
               '@ptel.com', '@text.republicwireless.com',
               '@tms.suncom.com', '@message.ting.com', '@email.uscc.net',
               '@cingularme.com', '@cspire1.com', '@vtext.com']'''
        lst = ['@txt.att.net', '@tmomail.net', '@messaging.sprintpcs.com',
               '@pm.sprint.com']
        for i in lst:
            fullNumber = str(number) + i
            self.to_List.append(fullNumber)
        

    def sendText(self, message, filePath = None, attachment = None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(self.to_List)
            msg['Subject'] = 'Message from Rubinstein Law Office'
            msgBody = message
            msg.attach(MIMEText(msgBody, 'plain'))
            if attachment:
                img = open(filePath, 'rb')
                base = MIMEBase('application', 'octet-stream')
                base.set_payload((img).read())
                encoders.encode_base64(base)
                msg.attach(base)
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            print(text)
            server.send_message(msg)
            #server.sendmail(self.username, self.to_List, text)
            #text = msg.as_string()
            #server.sendmail(fromaddr, toaddr, text)
            return True
            server.quit()
        except smtplib.SMTPException as e:
            log.loggingWarning(e, 'textMessage.py', 'sendText failed')
            return False
        
        
        
        
        
