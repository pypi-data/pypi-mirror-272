
from __future__ import annotations
import os
import typing_extensions
from typing import Union, cast, Any, Optional, TypeVar,Callable, TypedDict, cast
from datetime import datetime
from copy import deepcopy ,copy
import shutil
import operator
#import pandas as pd
#import numpy as np
import pytz
import re	

import bindfiles.tools.search_engine as loc
from bindfiles.tools.funcs import flat as fflat, path_join, NAME_FOLDER_SEP, path_normpath
from bindfiles.api.drive import File, File_Extra_Fields, Drive, File_to_drive, File_from_drive
from bindfiles.gclient.drive_v3 import File as DFile
import bindfiles.api.creds as gcred
NAME_FOLDER_SEP_DELETED = '¢££'

#File = Union[DFile, LFile]
#File_LIST = Union[list[File], list[DFile], list[LFile]]

STORAGE_NAMES = typing_extensions.Literal['local','gdrive']

#class FILE_SOURCE(TypedDict, total = False): sugestão 2024-04-08
#    LOCAL_PATH : str
#    ID : str
#    CRED: str
#    FILTER : Callable[[str,bool],bool]



class opt_list(typing_extensions.TypedDict, total=False):
    exclude_file: list[str]
    exclude_folder: list[str]
    include_folder: list[str] #default: ['.*']
    include_file: list[str] #default: ['.*']
    local_names: bool #corrige nome GDrive incompatível com path local
    filter_item : Callable[[File],bool]


def filter__get_func(opt : opt_list) -> Callable[[File],bool]:

    def include_item( file : File ) ->bool:
        ft_in, ft_out = opt.get('include_file',None), opt.get('exclude_file', None)
        if file.get('childs', None) or not file.get('isfile', True):
            ft_in, ft_out = opt.get('include_folder',None), opt.get('exclude_folder',None)

        b = True if not ft_in else False

        if ft_in:
            for fi in ft_in:
                if re.search(fi, file['name']):
                    b = True
                    break
        
        if b and ft_out:
            for fe in ft_out: 
                if re.search(fe, file['name']):
                    b = False
                    break
        return b
    
    return include_item


class source:
    ''' aqui lida parcialmente com questão de lidar com tipo de arquivo local e tipo do gdrive
        opções de cópia ficaram de fora pois não encapsulei aqui write_blob, get_blob e equivalentes    
    '''
    FIELDS = 'id,name,mimeType,parents,modifiedTime,size,md5Checksum,trashed' #+ ',isfile,folder' #gdrive + 'id,name,mimeType'
    EXTRA_FIELDS = 'isfile,folder'

    def __init__(self, folder:str, *,  cred:Optional[str] = None, options : opt_list = {}, stg_id : str = '' ):

        self.drive :Optional[Drive] = None

        self.root:Optional[str] = None
        self.paths:set[str] = set()        

        self._opt : opt_list = options

        self.root_file : File = {}
        
        if cred:
            self.drive = Drive(gcred.load(key=cred, id= stg_id))   
            self.root =  self.drive.get_id_from_url_string(folder)
            
        elif os.path.isdir(folder):
            self.root = path_normpath(folder)
        else:
            raise ValueError('Parâmetros inválidos para inicializar diretório')
        
        self.root_file['id'] = self.root
        self.root_file['childs'] = []
        self.root_file['folder'] = '' #root não costuma ter 'parent' mas sem 'folder' quebra funções
        self.lt_files : list[File] = self.root_file['childs']


    def listar(self, flat: bool ) -> list[File]:
        
        filter_func : Optional[Callable[[File],bool]] = self._opt.get('filter_item',None)
        if filter_func is None:
            filter_func = filter__get_func(self._opt)
        
        if self.drive and self.root:
            #print('listar drive')
            root_id = self.root
            lt_drive = self.drive.list_files( root_id, key_folder='', fields= source.FIELDS, flat = flat, filter= filter_func)

            if self._opt.get('local_names',True):
                lt_drive  = Drive.files_with_local_allowed_names( lt_drive )
                
            self.lt_files[:] = lt_drive
            #self._drive__dic_id = source.__drive__dict_folder(lt_drive, root_id )
            #os.__dict__['td'] = self._drive__dic_id

            
            return self.lt_files
        elif self.root:
            #print('listar local', self.root)
            self.lt_files[:] = loc.list_files(self.root, key_folder='',  fields= source.FIELDS, flat = flat, filter= filter_func)  #,folder 'modifiedTime,size'
            #self.lt_files = cast(list[File],fflat(lt_local,remove=True, add_folder= True))
            return self.lt_files
        else:
            raise RuntimeError()
        
    '''
    no download do gdrive: ns.isodate_gdrive_to_local(df) = modifiedDateTime
    
    '''
    @staticmethod
    def search_list(root_file :File, *, id: Optional[str] = None, path: Optional[str] = None ) -> Optional[File]:

        if path == '' or id == root_file['id']:
            return root_file

        ret : Optional[File] = None

        def seek(lt : list[File] ) -> None:
            nonlocal ret

            for f in lt:
                if ret:
                    return

                if id:
                    if f['id'] == id:
                        ret = f
                    elif 'childs' in f:
                        seek(f['childs'])
                
                if path:
                    f_path = path_join(f['folder'] , f['name'])
                    if f_path == path:
                        ret = f
                    elif 'childs' in f and path.startswith(f_path):
                        seek(f['childs'])
        seek(root_file['childs'])
        return ret
    
    @staticmethod
    def remove_from_list(root_file :File, *, id: Optional[str] = None, path: Optional[str] = None ) -> None:

        #print('REMOVE FROM LIST\n',f'id={id}', f'path={path}')
        if path == '' or id == root_file['id']:
            root_file['childs'][:] = []
            #return

        def seek_remove(lt : list[File] ) -> None:
            for f in lt:

                if id:
                    if f['id'] == id:
                        lt[:] = [i for i in lt if i['id'] != id]
                    elif 'childs' in f:
                        seek_remove(f['childs'])
                
                if path:
                    f_path = path_join(f['folder'] , f['name'])
                    if f_path.startswith(path):
                        lt[:] = [i for i in lt if i != f]
                    elif 'childs' in f and path.startswith(f_path): #potencial
                        seek_remove(f['childs'])
        seek_remove(root_file['childs'])

    #NÃO USADO
    def __deprecated__path_isdir(self, path:str ) -> bool: 
        if path == '':
            return True
        
        if self.drive:
            pid = source.search_list(self.root_file, path = path)
            return True if pid else False

        elif self.root:
            return os.path.isdir(path_join(self.root,path))
        else:
            raise RuntimeError()
        
    
    def _lprint(self, lt : Optional[list[File]] = None ) -> None:
        
        lt_ = lt if lt is not None else self.lt_files
        
        for i in lt_:
            print(f"{path_join(i['folder'],i['name'])}{'/' if not i['isfile'] else ''}")
            
            if 'childs' in i:
                self._lprint(i['childs'])
    
    
    def create_file(self, name : str, path : str,  blob: bytes, mimeType: Optional[str] = None) -> File:
        if self.drive:
            #return self.drive.file_content(file['id']) # type: ignore #Drive File
            parent_id = self.path_makedirs(path)['id']            
            fd = self.drive.upload_file( name=name, parents_id=parent_id, mimetype=mimeType, blob= blob, fields= self.FIELDS )
            #from time import sleep
            return File_from_drive(path, fd)

        elif self.root:
            fullname = path_join( self.root, path, name ) #NAME_FOLDER_SEP.join(path.split(NAME_FOLDER_SEP))
            folder = path_join( self.root,path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open( fullname ,'wb') as f:
                f.write(blob)
            return loc.info_file( fullname , self.FIELDS, self.root)
        else:
            raise RuntimeError()             
        
    def update_file(self, target : File, source : File, fields : str) -> File:
        
        d = { k:v for k,v in source.items() if k in fields.split(',') and k not in [ *File_Extra_Fields] } #'id',
        #d = { k:v for k,v in source.items() if k in fields.split(',') and k not in [ *File_Extra_Fields] } #'id',
        if self.drive:
            #if 'modifiedTime' in d:
            #    d['modifiedTime'] = f'{str(d["modifiedTime"])[0:19]}.000Z'

            dfile =  self.drive.update_file(file_id=target['id'], body= cast(DFile, d), fields=self.FIELDS)
            return File_from_drive(target['folder'], dfile )
            #return self.drive.file_content(file['id']) # type: ignore #Drive File
        elif self.root:
            
            return loc.update_file(target['id'],source=source, fields=self.FIELDS, root=self.root)
        else:
            raise RuntimeError()        
    
    def path_makedirs(self, path :str ) -> File: 

        if path == '':
            return self.root_file
        
        if self.drive:
                
                lt_path_name = path.split(NAME_FOLDER_SEP)
                pfile = self.root_file
                
                for folder_name in lt_path_name:
                    
                    next_pfile : Optional[File] = None
                    for fp in pfile['childs']:
                        if 'childs' in fp and fp['name'] == folder_name:
                            next_pfile = fp
                            break
                    
                    if next_pfile == None:
                        fdrive_new = self.drive.create_folder(parents_id=pfile['id'], name=folder_name, fields= self.FIELDS)
                        folder = path_join(pfile['folder'], folder_name)
                        next_pfile = File_from_drive(folder, fdrive_new)
                    
                    pfile['childs'].append( cast(File, next_pfile) )
                    pfile = cast(File, next_pfile) 
                
                return pfile

        elif self.root:
            full_folder = path_join(self.root,path)
            if not os.path.isdir(full_folder):
                os.makedirs(full_folder)
            return loc.info_file(full_folder,self.FIELDS,self.root)
        else:
            raise RuntimeError()
        

    #def path_isfile(self, path: str) -> bool: #type: ignore
    #    if self.drive:
    #        ...
    #    elif self.root:
    #        ...
    #   else:
    #        raise RuntimeError()    
        
    #def path_info(self, path: str) -> bool: #type: ignore
    #    if self.drive:
    #        ...
    #    elif self.root:
    #        ...
    #    else:
    #        raise RuntimeError()
        
    def path_delete(self, path: str) -> bool: #type: ignore
        if self.drive:
            fdel = source.search_list(self.root_file,path=path)
            if fdel:
                self.drive.delete_file(fdel['id'])
            else:
                raise RuntimeError()
        elif self.root:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        else:
            raise RuntimeError()
        source.remove_from_list(self.root_file, path=path)
        

    '''
    if os.path.isdir(local_path):
                shutil.rmtree(local_path)
            else:
                os.remove(local_path)
    s.drive.delete_file(f['id'])
    shutil.copyfile(pA,pB)
    os.makedirs(pA)

    '''
    def file_delete(self, fileId : str) -> None: 
        if self.drive:
            self.drive.delete_file(fileId)
        elif self.root:
            if os.path.isdir(fileId):
                shutil.rmtree(fileId)
            else:
                os.remove(fileId)
        else:
            raise RuntimeError()
        source.remove_from_list(self.root_file, id =fileId)

    
    #def __is_path_deleted(self,path:str) -> bool:
    #    path = path.replace(NAME_FOLDER_SEP,NAME_FOLDER_SEP_DELETED)
    #    for dp in self.__deletd_paths:
    #        if re.search(f'^{dp}',path):
    #            return True
    #    return False

    
    
    def __deprecated__info_file(self, file_id: str , *, check : bool = False) -> File:
        if self.drive:
            fid = self.search_list(self.root_file, id=file_id)
            if fid:
                return fid

            if check:
                f = self.drive.get(file_id, self.FIELDS) #aqui pega definições, menos "folder"
                for pid in f['parents']:
                    lt_path : list[tuple[str,str]] = []            
                    full_path = self.drive.folder_path__from_pid(pid, lt_pathId=lt_path)
                    for i,p in enumerate(lt_path):
                        if p[1] == self.root_file['id']:
                            folder = NAME_FOLDER_SEP.join( [t[0] for n,t in enumerate(lt_path) if n > i] )
                            return File_from_drive(folder, f)
            
            raise RuntimeError()
            
        elif self.root:
            return loc.info_file( file_id, self.FIELDS, self.root)
        else:
            raise RuntimeError()
     
    

    
    #def __add_deleted_path(self,path:str) -> None:
    #    ''' caminho foi excluído, o que implica exclusão de demais pastas e arquivos subordinados
    #        adicionar aqui serve para evitar comando de exclusão para estes itens já apagados
    #    ''' 
    #    self.__deletd_paths.add(path.replace(NAME_FOLDER_SEP,NAME_FOLDER_SEP_DELETED))   

    def get_blob(self, file_id: str) -> bytes:
        if self.drive:
            return self.drive.file_content(file_id)
        elif self.root:
            with open(file_id,'rb') as f:
                return f.read()
        else:
            raise RuntimeError()        
        
    def write_blob(self, file: File, blob : bytes) -> File:

        if self.drive:
            fd = self.drive.update_file(file_id=file['id'], mimetype=file['mimeType'],  blob = blob, fields= self.FIELDS) #file=file,            
            return File_from_drive(file['folder'],fd)
        
        elif self.root: 
            open(file['id'],'wb').write(blob)
            return loc.info_file(file['id'], fields=self.FIELDS ,root= self.root)
        else:
            raise RuntimeError()                
        
    
    #@staticmethod
    #def __drive__dict_folder( lt_files : list[File], root : str) -> dict[str,str]:
    #    dic = { path_join(f['folder'],f['name']) : f['id']  for f in lt_files if not f['isfile'] }
    #    dic[''] = root
    #    return dic
    


    
        
        



#class source_old(source):
#    def _source_check(self,place:STORAGE_NAMES) -> bool:
#            if place == 'gdrive' and self.drive:
#                return True
#            elif place == 'local' and self.root:
#                return True
#            else:
#                return False
#    
#    def local_path(self, subpath:str = '') -> str:
#        if self.root is not None:
#            return path_join(self.root,subpath)
#        raise RuntimeError()
#
#    def id(self, subpath:str = '') -> str:
#        if self.drive:
#            return self._drive__dic_id[subpath]
#        raise RuntimeError()   
