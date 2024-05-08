
from datetime import datetime , timezone
import os
#import re 
#import pandas as pd
import hashlib
from copy import copy

import typing
from typing import Union, Callable,Any, cast, Optional, Iterator, TypeVar

from bindfiles.api.drive import File
from bindfiles.tools.funcs import  path_join, path_normpath, NAME_FOLDER_SEP

#import pathlib

#from tesouraria.library.bindfiles.gclient.drive_v3 import File as GFile
import typing_extensions

class FileBase_0(typing_extensions.TypedDict, total=False):
    createdTime: str
    description: str
    fileExtension: str
    md5Checksum: str
    mimeType: str
    modifiedTime: str
    name: str
    sha1Checksum: str
    sha256Checksum: str
    size: int #type
    #ext : str
    folder: str #ADDED    
    kb : int #ADDED
    childs : list['FileBase_0']
    isfile: bool
    fullname: str #added


class _FileFields:
    def __init__(self,fields:str, *, extra : bool = False) -> None:
        lt = fields.split(',')
        self.id : bool = 'id' in lt
        self.createdTime : bool = 'createdTime' in lt
        self.description: bool = 'description' in lt
        self.fileExtension: bool = 'fileExtension' in lt
        self.md5Checksum: bool = 'md5Checksum' in lt
        self.mimeType: bool = 'mimeType' in lt
        self.modifiedTime: bool = 'modifiedTime' in lt
        self.name: bool = 'name' in lt
        self.sha1Checksum: bool = 'sha1Checksum' in lt
        self.sha256Checksum: bool = 'sha256Checksum' in lt
        self.folder: bool  = 'folder' in lt  or extra
        self.size: bool = 'size' in lt #type
        self.kb : bool = 'kb' in lt
        self.isfile : bool = 'isfile' in lt or extra
        self.fullname : bool = 'fullname' in lt


LEVEL_NONE = -1

def hashfile(file:str, hash: 'hashlib._Hash') -> str:
    BUF_SIZE = 65536
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

def list_files( root:str, fields:str, level:int = LEVEL_NONE, flat:bool = False,  add_folder : bool = True,
               filter : Optional[Callable[[File],bool]] = None, key_folder :str = '' ) -> list[File]:
    
    lt_root :list[File] = []
    
    
    fd = _FileFields(fields, extra=True)

    root = path_normpath(root)


    dic_childs : dict[str,list[File]] = { key_folder : lt_root }

    queue : list[tuple[str,int]] = []
    queue.append((key_folder,0))
    
    while len(queue) >0:
        folder, sl = queue.pop(0)
        lt = lt_root if flat else dic_childs[folder]        
        
        folder_sysname = path_join(root,folder)
        for li_name in os.listdir(folder_sysname): #, lt_dir, lt_file
            

            sysname = path_join( folder_sysname, li_name)
            is_dir = not os.path.isfile(sysname)

            pathname = path_join( folder, li_name) #acima do root
            fi :File = {'id':sysname , 'folder': folder}                                
            _set_field(fi, fd, root)

            if filter and not filter(fi):
                continue
            
            if is_dir: #if os.path.isdir(fullname):
                if level == LEVEL_NONE or sl + 1 <= level:
                    queue.append( (pathname ,sl + 1))
                    if not flat:
                        dic_childs[pathname] = fi['childs'] = []
                        #dic_childs[folder].append(fi)
            
            
            lt.append(fi)
                        
    return lt_root

def info_file( id: str, fields: str, root:str ) -> File:
    file : File = { 'id' : path_join(root,id ) }
    fd = _FileFields(fields)
    _set_field(file, fd, root)
    return file


def add_fields( lt:list[File], fields:str , root:str) -> None:

    if len(lt) == 0:
        return
    
    fd = _FileFields(fields)
    
    queue : list[tuple[str,list[File]]] = []
    queue.append(('',lt))
    
    while len(queue) >0:

        folder, lt = queue.pop(0)
        for file in lt:

            if 'childs' in file:
                subfolder = path_join(folder,file['name'])
                queue.append((subfolder,file['childs']))
            else:
                _set_field(file,fd, root)

def relative_to(from_folder:str, to_folder:str) ->str:
        #return str(pathlib.Path(to_folder).relative_to(pathlib.Path(from_folder)))
        _from_folder= path_normpath(from_folder).upper()
        _to_folder= path_normpath(to_folder).upper()
        lf = len(_from_folder)
        if lf <= len(_to_folder) and _from_folder == _to_folder[0:lf]:
            return to_folder[lf+1:]
        else:
            raise RuntimeError(f'pasta {to_folder} não provém de {from_folder}')

def _set_field( file:File, fd:_FileFields, root:str) -> None:
    
    fullname = file['id']

    
    if not os.path.exists(fullname):
        print('não achou\n',fullname)
        raise RuntimeError()
    
    #if fd.folder:
    #    file['folder'] = folder
    #if fd.id:
    #    file['id'] = fullname
    if fd.name:
        file['name'] = fullname.split(NAME_FOLDER_SEP)[-1]

    if fd.folder:
        full_folder =  NAME_FOLDER_SEP.join(fullname.split(NAME_FOLDER_SEP)[0:-1])
        file['folder'] = relative_to(root, full_folder) 

    if fd.size:                    
        file['size'] = str(os.path.getsize(fullname))
    #if fd.kb:
    #    size = os.path.getsize(fullname)
    #    file['kb'] = int(round(size / 1024))
    if fd.createdTime:
        #datetime.utcfromtimestamp(os.path.getctime(fullname)).isoformat() #https://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python
        timestamp = os.path.getctime(fullname)
        file['createdTime'] =  datetime.fromtimestamp(timestamp).isoformat().split('+')[0] #CHECK REMOVE #, timezone.utc
    if fd.modifiedTime:
        #ta = datetime.utcfromtimestamp(os.path.getmtime(fullname)).isoformat() 
        timestamp = os.path.getmtime(fullname)
        file['modifiedTime'] = datetime.fromtimestamp(timestamp, timezone.utc).isoformat().split('+')[0]
    #if fd.fileExtension:
    #    file['fileExtension'] = os.pa th.splitext(fullname)[-1] #item.split('.')[-1] #filename, ext = 
    if fd.isfile:
        file['isfile'] = os.path.isfile(fullname)

    
    if os.path.isfile(fullname):
        
        if fd.sha1Checksum:
            file['sha1Checksum'] = hashfile(fullname,hashlib.sha1())
        if fd.sha256Checksum:
            file['sha256Checksum'] = hashfile(fullname,hashlib.sha256())
        if fd.md5Checksum:
            file['md5Checksum'] = hashfile(fullname,hashlib.md5())


def update_file(fid: str,  source : File, fields : str, root:str) -> File:
    
    cf = info_file(fid,fields=fields,root=root )
    
    if 'modifiedTime' in cf and  cf['modifiedTime'] != source['modifiedTime']:
        mod = datetime.fromisoformat(source['modifiedTime']).timestamp()
        os.utime(fid,(mod,mod)) #último acesso e modificação

    if 'createdTime' in cf and  cf['createdTime'] != source['createdTime']:
        change_file_times_windows(fid,source['createdTime'])

    if 'name' in cf and cf['name'] != source['name']:
        novo_nome = path_join(cf['folder'], source['name'])        
        os.rename(fid, novo_nome)
        fid = novo_nome
    
    return info_file(fid, fields, root)



def change_file_times_windows(filepath: str, create_time: Any = None, access_time: Any = None, modify_time: Any = None) -> None:
    import pywintypes, win32file, win32con
    handle = win32file.CreateFile(
        filepath, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None
    )

    if create_time:
        create_time = pywintypes.Time(create_time)
    if access_time:
        access_time = pywintypes.Time(access_time)
    if modify_time:
        modify_time = pywintypes.Time(modify_time)

    win32file.SetFileTime(handle, create_time, access_time, modify_time) # type: ignore
    handle.close()
