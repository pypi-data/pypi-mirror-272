
#%%
#https://code.visualstudio.com/docs/python/jupyter-support-py  https://code.visualstudio.com/docs/python/jupyter-support-py
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


#https://stackoverflow.com/questions/59522335/how-we-can-use-google-sheet-api-to-update-the-sheet-with-new-data-using-python



from __future__ import annotations


#from __future__ import print_function

import base64
import os
import os.path
from datetime import datetime, timezone



from typing import Any, cast, Union, Callable, Optional, Protocol, Generic,TypeVar
from abc import ABC, abstractmethod
import io

from googleapiclient.discovery import build

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from bindfiles.api.creds import load
from bindfiles.tools.funcs import flat, path_normpath, path_join, NAME_FOLDER_SEP
from google.oauth2.credentials import Credentials #novo

from bindfiles.gclient.drive_v3 import ( 
    FileList, File as DFile, FileBase, Permission 
) #C:\Users\Christoph Cury\AppData\Roaming\Python\Python39\site-packages\googleapiclient-stubs\_apis\drive\v3

import typing
import typing_extensions
import sys
from copy import copy
import mimetypes

#https://www.datacamp.com/tutorial/inner-classes-python VER Inner

import re
#import pandas as pd
#import numpy as np
import bindfiles.api.rest_build as rest_build


MIMETYPE_FOLDER = 'application/vnd.google-apps.folder'
TEMP_INVALID_PATH = '%#@'


SPACES = typing_extensions.Literal['drive', 'appDataFolder','photos']
#https://github.com/polzerdo55862/google-photos-api/blob/main/Google_API.ipynb

File_Extra_Fields = ['folder','childs','isfile']

class File(FileBase, total=False):
    folder : str
    #kb : int 
    childs : list['File'] #incluído se não for flat
    isfile: bool
    #slan: str #system local allowed name


def File_from_drive( folder_path: str, file : FileBase) -> File:
    fb = cast(File, file)   
    fb['folder'] = folder_path
    
    fb['isfile'] = not fb.get('mimeType') == MIMETYPE_FOLDER
    if not fb['isfile']:
        fb['childs'] = []  # inicializa como lista vazia, assumindo que pode ser populado depois

    return fb

def File_to_drive( file : File ) -> DFile :    
    fd : DFile = cast(DFile, {k: v for k, v in file.items() if k not in File_Extra_Fields})
    return fd


class _FileFields:
    def __init__(self,fields:str) -> None:
        lt = fields.split(',')

        self.folder: bool  = 'folder' in lt #
        self.size: bool = 'size' in lt #type
        #self.kb : bool = 'kb' in lt
        self.isfile : bool = 'isfile' in lt
        #self.slan : bool = 'slan' in lt
NO_GDRIVE_FIELDS = 'folder,isfile'


if sys.platform.startswith('win'): #is_windows = 
    FORBIDEN = r'<>:"/\|?*'
else:
    FORBIDEN = r'/'


 #  fi['mimeType'] == 



LEVEL_NONE = -1

'''
T = TypeVar('T')

class Executor(Generic[T], ABC):
    @abstractmethod
    def execute(self) -> T: ...
    #pass

class DriveService(Protocol):
    def files(self) -> DriveFiles: ...

class DriveFiles(Protocol):
    def list(self, **kwds : Union[str,int]) -> Executor[FileList]: ...
    def create(self, **kwds : Any) -> Executor[FileList]: ...
'''

class Drive():
    

    def __init__(self, creds : Any) -> None:
        
        if isinstance(creds, Credentials) :
            self.service = build('drive', 'v3', credentials= creds)
            #creds = load(creds)
        else:
            self.service = rest_build.build_drive(creds) # type: ignore #build('drive', 'v3', token = creds)
            global MediaIoBaseDownload
            MediaIoBaseDownload = rest_build.MyMediaIoBaseDownload # type: ignore



    @staticmethod
    def local_allowed_name(name:str) ->str:
        #https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
        for c in FORBIDEN:
            if name.find(c) > -1:
                name = name.replace(c,' ')
        return name    
    
    @staticmethod
    def files_with_local_allowed_names(lt:list[File]) ->list[File]:
        for file in lt:
            file['name'] = Drive.local_allowed_name(file['name'])
            if 'childs' in file:
                file['childs'] = Drive.files_with_local_allowed_names(file['childs'])
        return lt
    
    def get_id_from_url_string(self,id_or_url:str) -> str:
        if Drive.is_folder_id(id_or_url):
            return id_or_url
                      #https://drive.google.com/drive/u/1/folders/1v-gN9v9_BXtMNRvjPb972rvO4qlhyZ2H
                      #'https://drive.google.com/drive/folders/([a-zA-Z0-9\_\-]+)'
        r = re.search('https://drive.google.com/drive.*?folders/([a-zA-Z0-9\_\-]+)',id_or_url) 
        if r:
            return r[1]
        elif re.search('root/',id_or_url):
            try:
                return self.folder_pid__from_path(id_or_url, folder_id= 'root')
            except Exception as e:
                print(e)
            
        raise ValueError(f'Padrão não reconhecido para id {id_or_url}')    
    
    
    
    @staticmethod
    def is_folder_id( id:str ) -> bool:
        m = re.search('[a-zA-Z0-9\_\-]+',id) 
        if not m:
            return False
        elif id != m[0]:
            return False
        return True #len(id) == 33 or len(id) == 73

        '''  Tamanhos do link:
        33 
        files & folder
        https://drive.google.com/file/d/17c8RXQTFNqbK4Ai72WEddApbjbcpT2M9/view
        https://drive.google.com/uc?id=17c8RXQTFNqbK4Ai72WEddApbjbcpT2M9&export=download

        44 aplicativos google
        https://docs.google.com/forms/d/1khtEs8Hw8cofFKD8xbNVEXIJUsSlj8Btv0wiPrMmhtg/edit
        https://docs.google.com/spreadsheets/d/1iqRGQpwGcDA0bzvT9zQrjHLIwHvmcsPuzo_4EAHDFM8/edit
        https://docs.google.com/document/d/1S7Oezjx21W6EK9TZKvrOYyUVxQNQ1Zy8GNRqKlWxyZk/edit

        73 pasta para cada anexo do formulário
        https://drive.google.com/drive/folders/1Gkl_6XoN5GW0n_FZTMx6w5kQdbFRrQycTubKS9rIKM1C7zG5k5J1zhtZggg0AeLhVLOQInJe

        49 algo compartilhado
        https://drive.google.com/file/d/0B1C6HXHNJZ9DcWFCekFPUzBKdl9PajFYcTdFV0lXbnNPdDhz/view?usp=drive_link&resourcekey=0-RGYTpQ5pYC55MhLLSG96AA
        https://drive.google.com/file/d/0B1C6HXHNJZ9DcWFCekFPUzBKdl9PajFYcTdFV0lXbnNPdDhz/view?resourcekey=0-RGYTpQ5pYC55MhLLSG96AA

        32 shortcut
        application/vnd.google-apps.shortcut

        28 
        https://docs.google.com/document/d/0B1C6HXHNJZ9DM3c4ZjMwejBTalU/edit?resourcekey=0-1I6FrecJWeEzz59slqsY7Q

        '''        

    @staticmethod
    def _minimal_recursive_fieldlist( fields:str ) ->str:
        ''' mímimo que precisa para identidade e diferenciar pasta de arquivo
            'id, name,webContentLink' #webViewLink  exemplo          
            https://developers.google.com/drive/api/v3/reference/files campos        
        '''
        fds = set(['id', 'name','mimeType'])
        if fields:
            fds.update(fields.split(','))
        return ','.join(fds)

    @staticmethod
    def _fieldlist_join(fa:str, fb:str ) ->str:
        fds = set(fa.split(',')); fds.update(fb.split(','))
        if '' in fds: fds.remove('')
        return ','.join(fds)
    
    @staticmethod
    def _fieldlist_remove(fl:str, fr:str ) ->str:
        fds = set(fl.split(',')); fds.difference_update(fr.split(','))
        if '' in fds: fds.remove('')
        return ','.join(fds)

    @staticmethod
    def flat(lf:list[File], remove : bool = True, add_folder: bool = True )-> list[File]:
        return flat(lf,remove=remove,add_folder=add_folder)


    def folder_pid__from_path(self, path : str, folder_id :str = 'root', dicpath : dict[str,str] = {} ) -> str: #dict[path,id]
        
        path_parts = path.split(NAME_FOLDER_SEP)
        dicpath[''] = ''
        current_folder_id = folder_id
        
        for folder_name in path_parts:
            cpath = NAME_FOLDER_SEP.join( (max(dicpath,key=len),folder_name) )
            if folder_name == 'root':
                continue
            response = self.service.files().list(
                q=f"'{current_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
                spaces='drive',
                fields='nextPageToken, files(id, name)',
            ).execute()
            files = response.get('files', [])
            if not files:
                raise RuntimeError( f'Não encontrado {folder_name} caminho {cpath}')
            else:
                #print(f'achou {folder_name} em { current_folder_id}')
                current_folder_id = files[0]['id']
                dicpath[cpath] = current_folder_id

        return current_folder_id    
    
    def folder_path__from_pid(self, pid: str, check_root : bool = True,
                              dicpath : dict[str,str] = {},  
                              lt_pathId : list[tuple[str,str]] = [] ) -> str:

        while True:
            file = self.get(pid,'id,name,parents,mimeType')
            lt_pathId.insert(0, (file['name'], file['id']) )
            if not 'parents' in file:
                pid = file['id']
                break
            pid= file['parents'][0]
        
        if check_root:
            froot = self.get('root','id,name,parents,mimeType')
            if froot['id'] == lt_pathId[0][1]:
                lt_pathId[0] = ('root', froot['id'])
        
        cur = ''
        for f in lt_pathId:
            cur = NAME_FOLDER_SEP.join([cur,f[0]])
            dicpath[cur] = f[1]
        
        return cur


    
    
    
    def list_files( self, id_folder:str, fields:str, key_folder:str = '', level:int = LEVEL_NONE, flat:bool = True, 
                   filter : Optional[Callable[[File],bool]] = None , add_folder : bool = True, trashed: bool = False) -> list[File]:
        
        fields = Drive._fieldlist_join(fields, 'id,name,mimeType,trashed')
        fields = Drive._fieldlist_remove(fields, NO_GDRIVE_FIELDS)
        lt_root :list[File] = []
        
        #fd = _FileFields(fields)
        #REMOVER NOMES QUE NÃO SÃO DO GDRIVE
        #if root_name: #normaliza '' como '.'
        #    root_name = o s.pa th.normpath(root_name)
        dic_childs : dict[str, list[File]] = { key_folder: lt_root }

        queue : list[tuple[str, str,int]] = []
        queue.append((id_folder,key_folder,0))
        
        while len(queue) >0:
            id_folder, folder, sl = queue.pop(0)
            lt = lt_root if flat else dic_childs[folder] 
            
            for dfi in self.get_items( fields, folder_id = id_folder ):
                #print('\n',dfi['name'],dfi)
                
                fi = File_from_drive(folder, dfi)
                
                fullname = fi['name'] if folder == '' else  NAME_FOLDER_SEP.join([folder, fi['name']])
                #if fd.folder: sempre tem item folder agora
                #    fi['folder'] = folder

                #is_folder = fi['mimeType'] == 'application/vnd.google-apps.folder'
                
                isFolder = not fi['isfile']
                if filter and not filter(fi):
                    #print('skiping', fi['name'])
                    continue                
                
                if isFolder:
                    if level == LEVEL_NONE or sl + 1 <= level:
                        queue.append( (fi['id'], fullname, sl+1 ))
                        
                        if not flat: #se for flat tudo é adicionado no lt_root
                            dic_childs[fullname] = fi['childs'] = []
                            #dic_childs[folder].append(fi)
                            
                if not isFolder or add_folder: #possivel listar incluindo apenas arquivos
                    lt.append(fi)                
        
        def filter_trashed(lt : list[File]) -> list[File]:
            lt2 = [ i for i in lt if i.get('trashed',False) == False ]
            for i in lt2:
                if 'childs' in i and len(i['childs']) > 0:
                    i['childs'] = filter_trashed(i['childs'])
            return lt2

        
        if not trashed:
            lt_root = filter_trashed(lt_root)
        return lt_root

    def get_all(self,fields:str = '', space: SPACES = 'drive', extra : Optional[dict[str,Any]] = None) -> list[File]:
        fields = Drive._fieldlist_join(fields,'id,name,parents')
        
        list_all = self.get_items(fields, space=space)

        tree : dict[str,list[File]] = {}
        folders : dict[str,File]  = {}

        lt_shared : list[File] = []
        lt_mult_parent : list[File] = []
        
        for _f in list_all: #step1 : identificar pastas e agrupar filhos
            
            f = File_from_drive(TEMP_INVALID_PATH, _f) 

            if 'parents' not in f:
                lt_shared.append(f)                
            else:
                n = len(f['parents'])
                if n != 1:
                    lt_mult_parent.append(f)
            
                for parent in f['parents']:
                    if not parent in tree:
                        tree[parent] = []
                    tree[parent].append(f)

        for _f in list_all: #step2 : criar árvore
            f = File_from_drive(TEMP_INVALID_PATH, _f) 
            #f = cast(File,f)
            if f['id'] in tree:
                folders[f['id']] = f
                f['childs'] = tree[f['id']]

        root = ''
        for t in tree:
            if t not in folders:
                root = t
        if extra:
            extra['root_id'] = root
            extra['shared'] = lt_shared
            extra['multi_parent'] = lt_mult_parent

        if root != '':
            return tree[root]
            
        #OPÇÃO SE NÃO ACHOU ROOT OU SE LISTA É VAZIA
        flat :list[File] = []
        for _f in list_all:
            f = File_from_drive(TEMP_INVALID_PATH, _f) 
            flat.append(f)
        return flat
    
    
    def get_items(self, fields:str, folder_id:Optional[str] = None, query:str = '', space: SPACES = 'drive') -> list[DFile]:
        '''
        query -> q="('1Ooba6zkxm-V5ADccM7iqwlPCu_2W_2st' in parents) and (name contains '1157' or name contains '1220')"
                #aceitou até uns 400 termos name contains or
        '''
        
        if query and folder_id:
            query = f"('{folder_id}' in parents) and ({query})"
        elif folder_id:
            query = f"('{folder_id}' in parents)"

        
        files :list[DFile] = []
        
        page_token :str = ''
        
        #print(query, space, page_token, fields)

        #lifdef verbose:ipage = 0
        while True:
            #C:\root\Python310\Lib\site-packages\googleapiclient-stubs\_apis\drive\v3\resources.pyi FilesResource list() linha 229
            results :FileList = self.service.files().list( #FilesResource list 
                q= query, 
                orderBy='name',
                spaces = space, #p['spaces']
                pageToken=page_token,
                pageSize = 1000,
                fields=f"files({fields}), nextPageToken" #incompleteSearch,
                ).execute()
            '''def searched_parent(dic:DFile) -> DFile:
                dic['appProperties'] = {AP_PARENT: folder_id}
                return dic
            
            if folder_id:
                results['files'] = [searched_parent(dic) for dic in results['files']]

            '''
            
            files.extend(results['files'])
            page_token = results.get('nextPageToken', '') #dict se não tiver retorna ''
            #lifdef verbose:ipage+=1;print('\t',ipage,folder_id)
            if page_token == '':
                break            
        return files
    
    def delete_file(self, id:str, *, remove_alternative : bool = True, pid : str = '') -> None:
        try:
            self.service.files().delete(fileId=id).execute()   
        except HttpError as error:
            self.move_file(id, remove_parents = pid)
    

    def rename_file(self, id:str, name:str ) -> None:
        #https://developers.google.com/drive/api/v3/reference/files/update
        #C:\root\Python310\Lib\site-packages\googleapiclient-stubs\_apis\drive\v3\resources.pyi FilesResource 
        file : DFile = self.service.files().update(fileId=id,body={"name":name},fields='id,name').execute()
        if file['name'] != name:
            raise RuntimeError(f'Nome não atualizado. desejado:"{name}" ,atual:"{file["name"]}')
        
    def move_file(self, id:str,*, folder_id:str = '', remove_parents:str = '') -> None:
        #https://developers.google.com/drive/api/guides/folder?hl=pt-br#create
        
        
        if not remove_parents:
            fpar : DFile = self.service.files().get(fileId=id, fields='parents').execute()
            remove_parents = ",".join(fpar['parents'] )
        
        file : DFile = self.service.files().update(fileId=id,addParents=folder_id,removeParents=remove_parents,fields='id,name,parents').execute()
        if folder_id and 'parents' in file and file['parents'] != folder_id.split(','):
            raise RuntimeError(f'Arquivo não movido. desejado:"{folder_id}" ,atual:"{",".join(file["parents"])}')
    
    def upload_file(self, name : str, parents_id:str , mimetype:Optional[str] = None,
                     full_path:Optional[str] = None, blob : Optional[bytes] = None,
                     fields:str = 'id') -> DFile:
        #https://developers.google.com/drive/api/guides/manage-uploads?hl=pt-br
        
        file_metadata : DFile = {'name': name, 'parents': parents_id.split(',')}
        
        media : Optional[Union[MediaFileUpload,MediaIoBaseUpload]] = None
        if full_path:
            #folder, name = os.path.split(full_path)
            media = MediaFileUpload( full_path, mimetype=mimetype, chunksize=5 * 1024 * 1024,resumable=True)  
            timestamp = os.path.getmtime(full_path) #datetime.utcfromtimestamp(os.path.getmtime(fullname))
            v1 = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()[0:19] + '.000Z' #.split('+')[0] + '.000Z'
            #print('----')
            #return
            file_metadata['modifiedTime'] = v1

        elif blob is not None:
            #if mimetype is None:
            #    raise ValueError("Mimetype must be provided when uploading bytes")
            
            if mimetype is None:
                mimetype = mimetypes.guess_type(name)[0]
                if mimetype is None:
                    mimetype = 'application/octet-stream'
            stream = io.BytesIO(blob)
            media = MediaIoBaseUpload(stream, mimetype=mimetype, resumable=True)  
            #sys.__dict__['media'] = media
            #return

        try:      
            file: DFile = self.service.files().create(body=file_metadata, media_body=media, fields=fields).execute()
            return file
        except Exception as e:
            print(f'Falha no Upload - {full_path} ',e)
            raise 

    def update_file(self, file_id: str, body: DFile = {},  mimetype:Optional[str]= None,
                     content_file:Optional[str] = None, blob : Optional[bytes] = None, 
                     fields:str = 'id') -> DFile:
        
        if 'modifiedTime' in body:
                body['modifiedTime'] = f'{body["modifiedTime"][0:19]}.000Z'
        
        args : dict[str,Any] = {'body':body, 'fields':fields}


        if mimetype is None:
            if 'mimetype' in body:
                mimetype = body['mimeType']
            elif 'name' in body:
                mimetype = mimetypes.guess_type(body['name'])[0]            
        
        media : Optional[Union[MediaFileUpload,MediaIoBaseUpload]] = None
        if content_file:
            #print('update file')
            media = MediaFileUpload(content_file, mimetype=mimetype, chunksize=5 * 1024 * 1024, resumable=True)
        elif blob is not None:
            #print('update data')
            #if mimetype is None:
            #    raise ValueError("Mimetype must be provided when uploading bytes")
            # Converte bytes para um stream que o MediaIoBaseUpload pode usar
            stream = io.BytesIO(blob)
            media = MediaIoBaseUpload(stream, mimetype=mimetype, resumable=True)        


        if media:
             args['media_body'] = media
             #media_body=media,

        try:      
            #C:\root\Python310\Lib\site-packages\googleapiclient-stubs\_apis\drive\v3\resources.pyi FilesResource 
            #file : DFile = self.service.files().update(fileId=id,body={"name":name},fields='id,name').execute()
            
            #fields é retorno
            #print(file)    
            
            updated_file: DFile = self.service.files().update(fileId= file_id, **args).execute() #REVER
            return updated_file
        except Exception as e:
            print(f'Falha no Uupdate - {body} {content_file} ',e)
            raise    

    def get(self, fileId:str, fields:str) -> DFile:
        return self.service.files().get(fileId=fileId, fields=fields).execute()

    def create_folder(self, parents_id:str,  name:str, fields:str = 'id') -> DFile:
        #https://developers.google.com/drive/api/guides/manage-uploads?hl=pt-br

        file_metadata : DFile = {'name': name, 'parents': parents_id.split(','), 'mimeType' : 'application/vnd.google-apps.folder' }
        fcreated: DFile = self.service.files().create(body=file_metadata, fields=fields).execute()
        return fcreated  

    def file_content(self, file_id:str) -> bytes:
        request = self.service.files().get_media(fileId=file_id)  # type: ignore
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request) #original ou overrided com rest_build -> ambos gravam em fh
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        return fh.getvalue()

    
    
    def downlad_file(self, file_id:str, filename:str, modified:Optional[datetime]) -> None:
        request = self.service.files().get_media(fileId=file_id)  # type: ignore
        fh = io.FileIO(filename, 'wb') # this can be used to write to disk
        downloader = MediaIoBaseDownload(fh, request) #original ou overrided com rest_build -> ambos gravam em fh
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            #print("Download %d%%." % int(status.progress() * 100))
        if modified:
            os.utime(filename,(modified.timestamp(),modified.timestamp())) #último acesso e modificação

    def fix_folders_same_name(self, lf: list[File]) -> list[File]:
        
        d_list: dict[str,list[File]] = {}
        d_uni: dict[str,File] = {}

        for file in lf:
            name = file['name']
            if 'childs' in file:
                if not name in d_list:
                    d_list[name] = [ file ]
                else:
                    d_list[name].append(file)

        for folder, lt_files in d_list.items():
            if len(lt_files) > 1:
                fid_unificado:File = lt_files[0]
                for fi in lt_files:
                    if len(fi['id']) < len(fid_unificado['id']):
                        fid_unificado = fi
                d_uni[folder] = fid_unificado

        
        lr: list[File] = [] #centralizar em um só nome - quando tem mais de um id para mesma pasta        
        
        for file in lf:
            name = file['name']
            add:bool = True
            if 'childs' in file and  len(d_list[name]) > 1:
                fid_unificado = d_uni[name]
                if fid_unificado['id'] != file['id']:
                    #diferente se não é onde vai ficar centralizado, tirar daqui
                    add = False
                    for child in file['childs']:
                        #print(f"movendo da pasta {file['name']} item {child['name']}")
                        self.move_file( child['id'], folder_id=fid_unificado['id'], remove_parents= file['id'])
                    self.delete_file(file['id'])
            if add:
                lr.append(file)

        
        for file in lr: #corrigir recursivamente
            if 'childs' in file:
                file['childs'] = self.fix_folders_same_name(file['childs'])

        return lr


                    
                    





                
        for fi in lt_files:
            if fi['id'] != fid_unificado['id']:
                for child in fi['childs']:
                    self.move_file( child['id'], fid_unificado['id'], fi['id'])





    #def download
    #https://stackoverflow.com/questions/59212443/google-drive-api-with-python-not-allowing-file-download-despite-correct-scopes-b

    #download de fotos
    #https://developers.google.com/photos/library/guides/access-media-items?hl=pt-br
    #https://developers.google.com/photos/library/reference/rest/v1/mediaItems/get?hl=pt-br

    #REVER
    def drive_remover_duplicatas(self, files: list[DFile]) -> None:
        print("conferir se tem duplicatas, nome iguais",len(files))
        sing: dict[str,str] = {}
        dupl: dict[str,str] = {}
        for f in files:
            n = f['name']
            if n in sing:
                dupl[n] = f['id'] #se já tem nome, vai para duplicata
            else:
                sing[n] = f['id'] #adiciona par nome:id

        if len(dupl)>0:
            lt_dupl :list[str] = [ dupl[n] for n in dupl ]
            print("remover", [n for n in dupl ])
            for id in lt_dupl:
                self.delete_file(id)


    def drive_file_compartilhar(self, idFile:Union[list[str],str], role:str ='reader') ->None:
        

        n:int = 0
        def add_per(file_id:str, ni: int) -> int:
            r = self.service.permissions().list(fileId = file_id).execute()
            """ Exemplo de retorno
            {'kind': 'drive#permission', 'id': 'anyoneWithLink', 'type': 'anyone', 'role': 'reader', 'allowFileDiscovery': False}
	        {'kind': 'drive#permission', 'id': '00085749206585731243', 'type': 'user', 'role': 'owner'}"""

            bTem = False
            for per in r['permissions']:
                if per['id'] == 'anyoneWithLink' and per['role'] == role:
                    bTem = True

            if bTem == False:
                print("Falso", file_id)
                bdy :  Permission = {'role': role, 'type': 'anyone'}   #, 'emailAddress': 'user@example.com'
                r2 = self.service.permissions().create( body = bdy, fileId = file_id,sendNotificationEmail= False, fields = 'id,type,role' #retorno
                    ).execute()
                print(r2)
                return ni+1
            return ni

        if type(idFile) == list:
            for f in idFile:
                n = add_per(f,n)
        elif type(idFile) == str:
            n = add_per(idFile,n)

        print(f"Atualizados: {n}")




    


