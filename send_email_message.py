#!/usr/bin/env python3

from email.message import EmailMessage
import os
import mimetypes
import smtplib
import csv


# This is your account credentials
detail_sender = {'name':'*****','email':'*******'}
mail_pass = '**** **** **** ****'

# Locate attachments, iterates all file in the attachment folder
# You should adjust the attachment_path here
attachment_path = "/home/Melegit/Automate mail/attachments/"
attachment_files = ([attachment_name for attachment_name in os.listdir(attachment_path) if '.jpeg' in attachment_name])


# Read the contact_list.csv, iterates all line and convert to dictionary
# An empty list also created, which is list_recipient. We add all dictionary from iterating to this list
list_recipient = []
with open('contact_list.csv', 'r') as file:
  csv_read = csv.DictReader(file)
  for line in csv_read:
    recipt_dict = dict(line)
    for attachment_file in attachment_files:
      if attachment_file.split('.')[0] in recipt_dict['attch_id']:
        recipt_dict['attachment'] = attachment_path + attachment_file
    list_recipient.append(recipt_dict) 


# Declare variable to assign all detail from list_recipient
for recipient in list_recipient:
  sender = detail_sender['email']
  recipient_email = recipient['email']
  recipient_attach = recipient['attachment']
  attachment_filename = os.path.basename(recipient_attach)

  # Setting up message to sent
  # You can edit the message['Subject'] and body as you want
  message = EmailMessage()
  message['From'] = sender
  message['To'] = recipient_email
  message['Subject'] = "Test 1. Greeting from {} to {}".format(detail_sender['name'], recipient['name'])
  body = """Hey there!
          I'm testing send email with attachment to many recipient using Python."""
  message.set_content(body)

  print(message)

  # we add attachment to the message
  mime_type, _ = mimetypes.guess_type(recipient_attach)
  mime_type, mime_subtype = mime_type.split('/', 1)

  with open(recipient_attach, 'rb') as ap:
    message.add_attachment(ap.read(),
			maintype = mime_type,
			subtype = mime_subtype,
			filename = attachment_filename)

  # Contact the mail server and then send all the message
  mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
  mail_server.login(sender, mail_pass)
  mail_server.send_message(message)
  mail_server.quit()
