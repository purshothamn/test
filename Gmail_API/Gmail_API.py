import pickle
import mimetypes
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

path = '/home/vsts/test/test/Gmail_API/'
SCOPES = ['https://mail.google.com/']

creds = None

if os.path.exists(path+'token.pickle'):
    with open(path+'token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            path+'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open(path+'token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

class Gmail_API:
    def __init__(self):
        self.service = service
    def getLabel(userId='me',i=''):

        if len(i) > 0:
            results = service.users().labels().list(userId=userId,id=i).execute()
        else:
            results = service.users().labels().list(userId=userId).execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])
    def getMailId(userId='me',labelIds=None,query=None,maxResults=None):

        messageIds = service.users().messages().list(userId=userId,labelIds=labelIds,q=query,maxResults=maxResults).execute()
        Ids = {}
        Ids['Ids'] = []
        Ids['resultSizeEstimate'] = messageIds['resultSizeEstimate']
        if messageIds['resultSizeEstimate'] == 0:
            return Ids
        for ids in messageIds['messages']:
            Ids['Ids'].append(ids['id'])
        return Ids
        
    def getMail(ids,userId='me'):

        message = service.users().messages().get(userId=userId,id=ids).execute()
        mailContain = message['payload']['headers']
        for i in mailContain:
            if i['name'] == 'From':
                From = i['value']
            if i['name'] == 'To':
                to = i['value']
            if i['name'] == 'Subject':
                Subject = i['value']
            if i['name'] == 'Date':
                Date = i['value']
        Body = message['snippet']
        # messageContent = {
        #                     'From': From,
        #                     'To': to,
        #                     'Subject': Subject,
        #                     'Date': Date,
        #                     'Body': Body
        # }
        return message
        
    def createMail(To, message_text, userId='me', From=None, Subject=None):

        if type(To) == list:
            for to in To:
                mimeContent = MIMEText(message_text)
                mimeContent['to'] = to
                mimeContent['from'] = From
                mimeContent['subject'] = Subject
                raw = base64.urlsafe_b64encode(mimeContent.as_bytes()).decode()
                body = {'raw': raw}

                service.users().messages().send(userId=userId, body=body).execute()
        else:
            mimeContent = MIMEText(message_text)
            mimeContent['to'] = To
            mimeContent['from'] = From
            mimeContent['subject'] = Subject
            raw = base64.urlsafe_b64encode(mimeContent.as_bytes()).decode()
            body = {'raw': raw}

            service.users().messages().send(userId=userId, body=body).execute()
    
    def deleteMail(ids, userId='me'):

        service.users().messages().delete(userId='me', id=ids).execute()
    
    def raw(ids, userId='me',fields='*'):

        message = service.users().messages().get(userId=userId,id=ids,fields=fields).execute()
        
        return message
