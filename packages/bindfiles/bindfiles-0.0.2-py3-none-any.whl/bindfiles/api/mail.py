
#%%
#https://code.visualstudio.com/docs/python/jupyter-support-py  https://code.visualstudio.com/docs/python/jupyter-support-py
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


#https://stackoverflow.com/questions/59522335/how-we-can-use-google-sheet-api-to-update-the-sheet-with-new-data-using-python



from __future__ import annotations


#from __future__ import print_function

#import oauth2client
#from oauth2client import client, tools
import base64
#import httplib2
import os
import os.path
import pickle
#needed for attachment
#import smtplib  
#import mimetypes
#from email import encoders
from email.message import Message
#from email.mime.audio import MIMEAudio
#from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import numpy as np

from typing import Any, cast, Union, Callable, Optional

from google.auth.transport.requests import Request as Transport_Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import builtins

from bindfiles.gclient.sheets_v4 import  ( Request as sheet_request, BatchUpdateSpreadsheetRequest, 
            BatchUpdateSpreadsheetResponse, GridProperties, GridRange, CellData, Color,
            ValueRange, UpdateValuesResponse, AppendValuesResponse, BatchGetValuesResponse,
            )

from bindfiles.gclient.drive_v3 import (
    FileList, File, Permission
)

from bindfiles.gclient.gmail_v1 import Message as gmail_message


#from sheets_v4 import Request as sheet_request, Response as sheet_response, sheet_request2, sheet_response2

#googleapiclient._apis.sheets.v4.schemas.BatchUpdateSpreadsheetRequest

"type g = googleapiclient._api"

import typing
import typing_extensions

#https://www.datacamp.com/tutorial/inner-classes-python VER Inner

import re
#import pandas as pd


AP_PARENT = 'parent'
AP_ROOT = 'root'


class Mail():

    def __init__(self, creds : Any) -> None:
        
        self.creds : Any
        self.service : Any  = build('gmail', 'v1', credentials= creds)
    
    
    
    def create_message_and_send(self, par:dict[str,str]) -> gmail_message:
        

        #<html><head></head><body>    </body></html>

        p = { 'sender':'','to':'', 'subject':'','text_plain':'','text_html':'','file':''}
        p = par

        msg = self.create_message_without_attachment(
            p['sender'], p['to'], p['subject'], p['text_html'], p['text_plain'])
        
        return self.send_Message_without_attachment("me", body= msg)                        

    def send_Message_without_attachment(self,user_id:str, body: gmail_message) -> gmail_message:
        service = build('gmail', 'v1', credentials= self.creds)
        try:
            message_sent = (service.users().messages().send(userId=user_id, body=body).execute())
            return  message_sent #['id']
            # print(attached_file)
            #print (f'Message sent (without attachment) \n\n Message Id: {message_id}\n\n Message:\n\n {message_text_plain}')
            # return body
        except Exception as e:
            raise RuntimeError("erro ao enviar") from e

    def create_message_without_attachment (self, sender:str, to:str, subject:str, message_text_html:str, message_text_plain:str) -> gmail_message:
        
        
        if len(message_text_html)==0:
            mt = MIMEText(message_text_plain)
            mt['Subject'] = subject
            mt['From'] = sender
            mt['To'] = to
            raw_message = base64.urlsafe_b64encode(mt.as_string().encode("utf-8"))
            return {
                'raw': raw_message.decode("utf-8")
            }
        else:
            mm = MIMEMultipart('mixed') #MIMEMultipart('alternative') #
            mm['Subject'] = subject
            mm['From'] = sender
            mm['To'] = to
            mm['Content-type'] = 'text/html; charset=iso-8859-1'

            mm.attach(MIMEText(message_text_plain, 'plain'))
            mm.attach(MIMEText(message_text_html, 'html'))


            raw_message_no_attachment = base64.urlsafe_b64encode(mm.as_bytes())

            return  {'raw': raw_message_no_attachment.decode("utf-8") }




