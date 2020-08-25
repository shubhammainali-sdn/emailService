
import logging
l = logging.getLogger(__name__)

import json
import smtplib,ssl

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import parseaddr
from email import encoders

from app import config 

def send_template_email(from_address,to_addresses, subject, files, tags=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = from_address
        l.info('from %s' % (msg["From"]))
        msg['To'] = ", ".join(to_addresses)
        l.info('to %s' % (msg["To"])) 
        msg["Subject"] = "Demo mail"
        if len(files)>0:
            for data in files:
                print(data.filename)
                attach_file_name = data.filename
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload(data.file.read())
                encoders.encode_base64(payload) 
                payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
                msg.attach(payload)
        if tags is not None:
            msg["X-MC-Tags"] = ",".join(tags)

        html = "<p>Welcome to the email service.This is a Demo mail</p>"
        part = MIMEText(html, 'html')
        msg.attach(part)
        s = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(config.USERNAME, config.PASSWORD)
        l.info("SMTP authentication Successfull")
        try:
            # s.sendmail(msg['From'], msg['To'], msg.as_string())
            l.info('mail send successfully..')
        except Exception as e:
            l.exception("could not deliver to address")
            # Silently eat it. Nothing we can do.

        s.quit()
    except Exception as e:
        l.exception(e)
