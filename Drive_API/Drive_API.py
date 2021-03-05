import httplib2
import os.path, io
import pickle,mimetypes

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

path = r'/home/vsts/test/test/Drive_API/'

SCOPES = ['https://www.googleapis.com/auth/drive']
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

drive = build('drive', 'v3', credentials=creds)

class Drive_API:
    def __init__(self):
        self.drive = drive

    def download(self,id,path=os.path.join(os.getcwd(), 'temp.tmp')):
        request = drive.files().get_media(fileId=id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        with io.open(path,'wb') as f:
            fh.seek(0)
            f.write(fh.read())
    
    def listFiles(self,parent=''):
        if len(parent) > 0:
            parent = self.searchFile(parent)[0]['Id']
            query = f"'{parent}' in parents"
            results = drive.files().list(q=query).execute()
        else:
            results = drive.files().list(fields="files(id, name)").execute()
        items = results.get('files', [])
        l = []
        n = 0
        if not items:
            return []
        else:
            for item in items:
                l.append({'Name':item['name'],'Id':item['id'],'index':n})
                n +=1
            return l
    
    def upload(self,files, mimetype='', folder_id=''):
        if (type(files) == list):
            pass
        else:
            files = [files]
        for file in files:
            try:
                if len(folder_id) > 0:
                    folder_id = folder_id
                    file_metadata = {
                        'name': file,
                        'parents': [folder_id]
                    }
                else:
                    file_metadata = {'name': file}
                if (len(mimetype) <= 0):
                    ext = os.path.splitext(file)[1]
                    mimetypes.init()
                    mimetypes.types_map[ext]
                    media = MediaFileUpload(file,
                                        mimetype=mimetype,
                                        resumable=True)
                file = drive.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
                Id = '%s' % file.get('id')
                return Id
            except Exception as err:
                Type = type(err)
                Type = str(Type).replace('<class ','').replace('>',':')
                print(Type,err)

    def createFolder(self,folder_name,folder_id=''):
        if type(folder_name) == list:
            pass
        else:
            folder_name = [folder_name]
        for name in folder_name:
            try:
                if len(folder_id) > 0:
                    file_metadata = {
                        'name': name,
                        'parents': [folder_id],
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                else:
                    file_metadata = {
                        'name': folder_name,
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                file = drive.files().create(body=file_metadata,
                                                    fields='id').execute()
                Id = '%s' % file.get('id')
                return Id
            except Exception as err:
                Type = type(err)
                Type = str(Type).replace('<class ','').replace('>',':')
                print(Type,err)

    def searchFile(self,query,findall=False,fields=None):
        if findall:
            query = 'name contains '+"'"+query+"'"
        else:
            query = 'name = '+"'"+query+"'"
        results = drive.files().list(fields=fields,q=query).execute()
        items = results.get('files', [])
        l = []
        n = 0
        if fields != None:
            return items
        else:
            if not items:
                print('No files found.')
            else:
                for item in items:
                    l.append({'Name':item['name'],'Id':item['id'],'index':n})
                    n +=1
                return l

    def deleteFile(self,id):
        try:
            response = drive.files().delete(fileId=id).execute()
        except Exception as err:
            return err
        else:
            return 'Successfully deleted'
    

    def fileUpdates(self,fileName,fields='files/lastModifyingUser'):

        response = self.searchFile(query=fileName,fields=fields)
        
        return response