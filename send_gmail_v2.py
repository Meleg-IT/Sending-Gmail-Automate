#!/usr/bin/env python3

import os
import mimetypes
import csv
from email.message import EmailMessage
import smtplib



detail_sender = {'name':'********','email':'******@*****'}
mail_pass = '**** **** **** ****'


attachment_path = "/****/*******/***********/*************/"
attachment_files = ([attachment_name for attachment_name in os.listdir(attachment_path)])


list_recipient = []
with open('contact_list_dev.csv', 'r') as file:
  csv_read = csv.DictReader(file)
  for line in csv_read:
    attachs = []
    for attachment_file in attachment_files:
      if attachment_file.split('.')[0] in line['attch_id']:
        attach_list = attachment_path + attachment_file 
        attachs.append(attach_list) 
    line["attachment"] = attachs
    list_recipient.append(line) 
print('list_recipient is: ', list_recipient)

for recipient in list_recipient:
  sender = detail_sender['email']
  recipient_email = recipient['email']
  recipient_attach = recipient['attachment']
  #print('recipient_attach is: ', recipient_attach)
			
  message = EmailMessage()
  message['From'] = sender
  message['To'] = recipient_email
  message['Subject'] = "Test 5. Greeting from {} to {}".format(detail_sender['name'], recipient['name'])
  body = """Hey there!
          I'm testing send email with multiple attachment to many recipient using Python."""
  message.set_content(body)
  
  for list_attach in recipient['attachment']:
    attachment_filename = os.path.basename(list_attach)
    mime_type, _ = mimetypes.guess_type(list_attach)
    mime_type, mime_subtype = mime_type.split('/', 1)
    with open(list_attach, 'rb') as ap:
      message.add_attachment(ap.read(), maintype = mime_type, subtype = mime_subtype, filename = attachment_filename)

  
  mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
  mail_server.login(sender, mail_pass)
  mail_server.send_message(message)
  mail_server.quit()
