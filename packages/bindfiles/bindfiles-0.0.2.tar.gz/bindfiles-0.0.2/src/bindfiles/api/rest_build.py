from __future__ import annotations

import requests
import requests.utils as ru
#ru.requote_uri
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.errors import HttpError
import json
import io

from typing import Callable, TypeVar, Generic, TypedDict, Literal, Optional, List, Any, cast, Union

from bindfiles.gclient.drive_v3 import ( 
    FileList, File as DFile, Permission
) 


class _expand_:
    def __init__(self,name:str) -> None:
        self.name = name

    def __getattr__(self, name:str) -> Any:
        
        print(f"O método '{name}' não foi implementado. em REST {self.name}")
        return lambda : _expand_( f'{self.name}.{name}')
    
T = TypeVar('T')

class Execute(Generic[T]):
    def __init__(self, fun: Callable[[], T]) -> None:
        self._func = fun

    def execute(self) -> T:
        return self._func()

class rest_drive(_expand_):
    def __init__(self,token:str) -> None:
        super().__init__('drive')
        self.token = token

    def files(self) -> rest_drive_files:
        return rest_drive_files(self.token)


class rest_drive_files(_expand_):
    def __init__(self,token:str) -> None:
        super().__init__('drive.files')
        self.token = token

    def list(self, **param :dict[str,Any]) -> Execute[FileList]:
        
        def func() -> FileList: #token: str, params: dict[str,Any]
            url = "https://www.googleapis.com/drive/v3/files"
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.get(url, headers=headers, params=param) 
            if resp.status_code != 200:
                raise RuntimeError(resp.reason) 
            return resp.json() # type: ignore
        return Execute( lambda : func() )
    
    
    def create(self,body : DFile, media_body : Union[MediaFileUpload,MediaIoBaseUpload,None] = None, 
               fields: str = '') -> Execute[DFile]: #FileList
        
        def func() -> DFile: #token: str, params: dict[str,Any]
                headers = { 'Authorization': f'Bearer {self.token}' }
                meta_data = json.dumps(body)                
                files = { 'metadata': ('metadata', meta_data, 'application/json') }

                if isinstance(media_body, MediaFileUpload): #json_file = media_body.to_json()
                    file_path = media_body._filename # type: ignore  #tem sim
                    mimetype = media_body._mimetype # type: ignore
                    files['file'] = (body['name'], open(file_path, 'rb'), mimetype) # type: ignore

                elif isinstance(media_body, MediaIoBaseUpload): #json_file = media_body.to_json()
                    mimetype = media_body._mimetype  # type: ignore

                    class br():
                        def read(self) -> bytes:
                            return media_body.getbytes(0,-1) # type: ignore
                        def close(self) -> None:... #pois podia ser arquivo aberto
                    
                    files['file'] = (body['name'], br(), mimetype) # type: ignore


                qfields = f"&fields={fields}" if fields else 'id'
                url = f'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart{qfields}'

                response = requests.post(url, headers=headers, files=files)
                if media_body and 'file' in files:  # Fechando o arquivo aberto se houver.
                    files['file'][1].close() # type: ignore
                
                return cast(DFile, response.json()) #['file']
        
        return Execute( lambda : func() )    
    
    def get_media(self, fileId : str ) -> requests.Response:
        url = f"https://www.googleapis.com/drive/v3/files/{fileId}?alt=media"
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers, stream=True)
        return response
    
    def delete(self, fileId : str ) -> Execute[None]:
        def func() -> None:
            url = f"https://www.googleapis.com/drive/v3/files/{fileId}"
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.delete(url, headers=headers)
            if response.status_code == 403:
                raise HttpError(resp=response, content=b'The user does not have sufficient permissions for this file.', uri=url)        
        return Execute (lambda : func() )        
    
    def update(self, fileId : str, *, fields : str, body: DFile = {} ,
                media_body : Any = None, #,MediaIoBaseUpload,None
                addParents: Optional[str] = None ,removeParents : Optional[str] = None ) -> Execute[DFile]:
        
        def func() -> DFile: #token: str, params: dict[str,Any]
                headers = { 'Authorization': f'Bearer {self.token}' }
                meta_data = json.dumps(body)                
                files = { 'metadata': ('metadata', meta_data, 'application/json') }

                if isinstance(media_body, MediaFileUpload): #json_file = media_body.to_json()
                    #p rint('uu file')
                    file_path = media_body._filename # type: ignore  #tem sim
                    mimetype = media_body._mimetype # type: ignore
                    files['file'] = ('exp', open(file_path, 'rb'), mimetype) # type: ignore

                elif isinstance(media_body, MediaIoBaseUpload): #json_file = media_body.to_json()
                    #p rint('uu data')
                    
                    mimetype = media_body._mimetype  # type: ignore

                    class br():
                        def read(self) -> bytes:
                            return media_body.getbytes(0,-1) # type: ignore
                        def close(self) -> None:... #pois podia ser arquivo aberto
                    
                    files['file'] = ('exp', br(), mimetype) # type: ignore  #exp = body['name']


                qfields = f"&fields={fields}" if fields else 'id'
                #url = f'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart{qfields}'
                parents_params = ""
                if addParents:
                    parents_params += f"&addParents={addParents}"
                if removeParents:
                    parents_params += f"&removeParents={removeParents}"

                url = f"https://www.googleapis.com/upload/drive/v3/files/{fileId}?uploadType=multipart{qfields}{parents_params}"

                response = requests.patch(url, headers=headers, files=files)
                if media_body and 'file' in files:  # Fechando o arquivo aberto se houver.
                    files['file'][1].close() # type: ignore
                
                
                # quando remove o parent (devolvendo arquivo para dono) retorno vem em branco
                ret : DFile = {}
                try:
                    ret = cast (DFile, response.json()) 
                except Exception as e:...
                
                return ret #['file']     

        return Execute( lambda : func() )   
    
    def get(self, fileId:str, fields:str) -> Execute[DFile]:
        def func() -> DFile:
            url = f"https://www.googleapis.com/drive/v3/files/{fileId}?fields={fields}"
    
            headers = { 'Authorization': f'Bearer {self.token}',
                'Accept': 'application/json'}  # Esperamos uma resposta em JSON
            
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                response.raise_for_status()
                raise RuntimeError(response.reason)
            
            #p rint(response.json())
            return cast(DFile, response.json())  # Retornando o conteúdo JSON da resposta

        return Execute( lambda : func() )   
        

def build_drive(token : str) -> rest_drive:
    return rest_drive(token)
        

class MyMediaIoBaseDownload:
    def __init__(self, file_io: io.FileIO, req: requests.Response):
        self.file_io = file_io
        self.req = req
        self.finished = False

    def next_chunk(self) -> tuple[int,bool]:
        if self.req.status_code == 200:
            for chunk in self.req.iter_content(chunk_size=4096):
                self.file_io.write(chunk)
            self.finished = True
            return (200, self.finished)
        else:
            return (self.req.status_code, self.finished)
        

#service.permissions().create( body = bdy, fileId = file_id,sendNotificationEmail= False, fields = 'id,type,role' #retorno).execute()


    '''
       q= query, 
                orderBy='name',
                spaces = space, #p['spaces']
                pageToken=page_token,
                pageSize = 1000,
                fields=f"files({fields}), nextPageToken" #incompleteSearch,
                

                q=f"'{current_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
                spaces='drive',
                fields='nextPageToken, files(id, name)',         

            corpora: str = ...,
            corpus: typing_extensions.Literal["domain", "user"] = ...,
            driveId: str = ...,
            includeItemsFromAllDrives: bool = ...,
            includeLabels: str = ...,
            includePermissionsForView: str = ...,
            includeTeamDriveItems: bool = ...,
            orderBy: str = ...,
            pageSize: int = ...,
            pageToken: str = ...,
            q: str = ...,
            spaces: str = ...,
            supportsAllDrives: bool = ...,
            supportsTeamDrives: bool = ...,
            teamDriveId: str = ...,                       
    
    '''




    



#C:\root\Python310\Lib\site-packages\googleapiclient-stubs\_apis\drive\v3\resources.pyi FileResource list linha 229
'''class ListParams(TypedDict, total=False):
    orderBy: str
    spaces: str
    pageToken: str
    pageSize: int
    fields: str
    q: str
    corpora: str
    corpus: Literal["domain", "user"]
    driveId: str
    includeItemsFromAllDrives: bool
    includeLabels: str
    includePermissionsForView: str
    includeTeamDriveItems: bool
    supportsAllDrives: bool
    supportsTeamDrives: bool
    teamDriveId: str
'''


#DEFAULT_FILE_FIELDS = 'id,name,modifiedTime,size,mimeType,trashed'






'''  abaixo implementação de programa e não low level
def list_from_parent(token: str, parentID: str, params: Optional[ListParams] = None, 
                     fields: Optional[str] = None, PageToken : Optional[str] = None) -> List[DFile]:
    if not params:
        params = {}

    query_fields = f"nextPageToken, files({ fields if fields else DEFAULT_FILE_FIELDS })"
    
    params.setdefault("fields", query_fields)
    
    search_filters = [f"('{parentID}' in parents)"]        

    if 'q' in params:
        search_filters.append(params['q'])
    params["q"] = " and ".join(search_filters)

    if PageToken:
        params["pageToken"] = PageToken        
    
    url = "https://www.googleapis.com/drive/v3/files"
        
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params)
        
    if resp.status_code != 200:
        return []
        #break
        
    data = resp.json()
    return data.get('files', [])




def list_from_parent2(token: str, parentID: str, parentName: str = '', fields: Optional[str] = None) -> List[DFile]:
  FIELDS = f"nextPageToken, files({ fields if fields else DEFAULT_FILE_FIELDS })"
  search = f"'{parentID}' in parents"
  fields = fields or f"nextPageToken,files({DEFAULT_FILE_FIELDS})"
  
  
  all_files:List[DFile] = []
  page_token = None
  while True:
    url = f"https://www.googleapis.com/drive/v3/files?q={requests.utils.quote(search)}&fields={requests.utils.quote(fields)}"
    if page_token:
      url += f"&pageToken={requests.utils.quote(page_token)}"
    
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        break
    
    data = resp.json()
    received_files = data.get('files', [])
    all_files.extend(received_files)  # Adapte conforme a estrutura do seu objeto File
    
    page_token = data.get('nextPageToken')
    if not page_token:
      break

  return all_files  # Adapte conforme necessário


def list_from_parent__extra_pt(token: str, parentID: str, params: Optional[ListParams] = None, 
                     fields: Optional[str] = None) -> List[DFile]:

    FIELDS = f"nextPageToken, files({ fields if fields else DEFAULT_FILE_FIELDS })"
    search = f"('{parentID}' in parents)"
    
    # Configuração padrão dos campos se não forem especificados
    if not params:
        params = {}
    params.setdefault("fields", FIELDS)
    params["q"] = search

    all_files:List[DFile] = []    

    page_token = None
    while True:
        #url = f"https://www.googleapis.com/drive/v3/files?q={requests.utils.quote(search)}&fields={requests.utils.quote(fields)}"
        url = "https://www.googleapis.com/drive/v3/files"
        if page_token:
            url += f"&pageToken={requests.utils.quote(page_token)}"
        
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, params=params)
        
        if resp.status_code != 200:
            break
        
        data = resp.json()
        received_files = data.get('files', [])
        all_files.extend(received_files)  # Adapte conforme a estrutura do seu objeto File
        
        page_token = data.get('nextPageToken')
        if not page_token:
            break

    return all_files  # Adapte conforme necessário
'''    
    
    
    
    
    








'''

sheets
from __future__ import annotations
from typing import Any, Optional, TypeVar, Generic, Any, cast, Callable
from typing_extensions import Literal
from urllib.parse import quote

import requests
import json


sheet_request = Any
BatchUpdateSpreadsheetRequest = Any
BatchUpdateSpreadsheetResponse = Any
GridProperties =  Any
GridRange = Any
CellData = Any
Color = Any
ValueRange = Any
UpdateValuesResponse = Any
AppendValuesResponse = Any
ClearValuesResponse = Any


#'sheets', 'v4', credentials= creds)

#se passar credentials é token ou url
def build( api:str, ver:str, credentials:Optional[Any] = None ) -> Service:
    return Service()


def run_request( read : Callable[[],requests.Response] ) -> Any:
    response = read()
    if response.status_code == 200:
        return response.json()
    else:
        p rint('\nstatus code:')
        p rint(response.status_code)
        p rint('\ntext:')
        from IPython.display import HTML,display, IFrame
        import base64
        
        html_resp = base64.b64encode(response.text.encode('utf-8')).decode('utf-8')
        display(HTML(f'<iframe src="data:text/html;base64,{html_resp}" width="1700" height="400"></iframe>')    )
        display(IFrame('<h1>VIDA2</h1>')    )
        IFrame('<h1>VIDA3</h1>') 
        display(IFrame(response.text)    )
        #p rint(response.text)
        p rint('\njson:')
        p rint(response.json)

        p rint('\nresponse:')
        p rint(response)
        raise Exception(f'Erro na API do Google Sheets: {response.status_code}')

class Service:

    def __init__(self) -> None:
        GAS_URL = 'https://script.google.com/macros/s/AKfycbzmYbaXp2kNvVMlD9_zsLpdDF0C9J5YrZghPSTDMApy5V_t1zU92Yyj9q6JA1teoSvVjw/exec?token'
        self.token = requests.get(GAS_URL).text
        self.header = {'Authorization': 'Bearer ' + self.token}
    
    def spreadsheets(self) -> Spreadsheet:
        return Spreadsheet(self)


T = TypeVar('T')

class Execute(Generic[T]):

    def __init__(self, func: Callable[[],T] ) -> None:
        self.func = func

    def execute(self) -> T:
        return cast(T, run_request(self.func)) # type: ignore


class Spreadsheet_Values:
    
    def __init__(self, serv:Service) -> None:
        self.serv = serv

    #.values().update(spreadsheetId=self.id, range=range,valueInputOption='USER_ENTERED', body=body).execute()
    def update(self, spreadsheetId:str, range:str, body: Any, 
               valueInputOption:Literal["INPUT_VALUE_OPTION_UNSPECIFIED","RAW","USER_ENTERED"] = 'USER_ENTERED',                
               ) -> Execute[UpdateValuesResponse]:
        #p rint('update ck')
        #return


        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}?valueInputOption={valueInputOption}'
        
        return Execute[ValueRange]( lambda : requests.put(url, headers=self.serv.header, data = json.dumps(body)) )

    #.values().append(spreadsheetId= self.id, range= range, valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body= bdy).execute()
    #.values().append(spreadsheetId= self.id, range=range,valueInputOption='RAW',insertDataOption = 'INSERT_ROWS', body=bdy).execute()
    def append(self, spreadsheetId:str, range:str, body: Any, 
               valueInputOption:Literal["INPUT_VALUE_OPTION_UNSPECIFIED","RAW","USER_ENTERED"] = 'USER_ENTERED',                
               insertDataOption:Literal["OVERWRITE","INSERT_ROWS"] ='INSERT_ROWS'
                 ) -> Execute[AppendValuesResponse]:
        
        range = quote(range)
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}:append?valueInputOption={valueInputOption}&insertDataOption={insertDataOption}'
        return Execute[ValueRange]( lambda : requests.post(url, headers=self.serv.header, data = json.dumps(body)) )

    
    #.values().get(spreadsheetId=self.id, range=range)    
    def get(self, spreadsheetId:str, range:str ) -> Execute[ValueRange]:
        range = quote(range)
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}'
        return Execute[ValueRange]( lambda : requests.get(url, headers=self.serv.header) )
    
    #.values().clear(spreadsheetId=self.id, range=range) #, body=clear_values_request_body)
    def clear(self, spreadsheetId:str, range:str) -> Execute[ClearValuesResponse]:
        range = quote(range)
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}:clear'
        return Execute[ValueRange]( lambda : requests.post(url, headers=self.serv.header) )


def convert_sheet_id_to_int(d: dict[Any,Any]) -> None:
    if isinstance(d, dict):
        for key, value in d.items():
            if key == 'sheetId' and isinstance(value, str):
                d[key] = int(value)
            else:
                convert_sheet_id_to_int(value)
    elif isinstance(d, list):
        for item in d:
            convert_sheet_id_to_int(item)


class Spreadsheet:

    def __init__(self, serv:Service) -> None:
        self.serv = serv

    def batchUpdate(self, spreadsheetId: str, body:BatchUpdateSpreadsheetRequest) -> Execute[BatchUpdateSpreadsheetResponse]:
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}:batchUpdate'
        #p rint('batchUpdate')
        import pp rint
        
        convert_sheet_id_to_int(body)
        #pp rint.pp rint(body)

        return Execute[BatchUpdateSpreadsheetResponse]( lambda : requests.post(url, headers=self.serv.header, data = json.dumps(body)) )

    def values(self) -> Spreadsheet_Values:
        return Spreadsheet_Values(self.serv)

    


'''