import smtplib,ssl
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER_HOST='localhost'
SMTP_SERVER_PORT=1025
SENDER_ADDRESS='snklpsrkr@gmail.com'
SENDER_PASSWORD="BlueLock1290"

context=ssl.create_default_context()

def email_send(to,sub,msg,attach=None):
    mail=MIMEMultipart()
    mail["from"]=SENDER_ADDRESS
    mail["subject"]=sub
    mail["To"]=to

    mail.attach(MIMEText(msg,"html"))

    if attach is not None:
        attach_file=open(attach,"rb")
        prt=MIMEBase("application","octet-stream")
        prt.set_payload(attach_file.read())
        encode_base64(prt)
        
        prt.add_header("Content",f"attachment: filename={attach}")

        mail.attach(prt)
    
    s=smtplib.SMTP(host='localhost',port=1025)
    #s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()
    
    return True