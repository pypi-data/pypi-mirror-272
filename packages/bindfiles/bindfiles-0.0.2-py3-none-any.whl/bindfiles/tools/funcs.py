
import requests
#import urllib
#import pandas as pd
import os
import re
from datetime import datetime,timedelta
#import sys #sys._getframe().f_lineno
#import numpy as np

#import source_swe as swe
from typing import Any, Union, TextIO, cast, TypeVar, Callable, Optional, List
from copy import copy

import sys
import importlib

#modulos desse projeto:
#from types import ModuleType
#import bindfiles


import re

NAME_FOLDER_SEP = '/'

def path_join(*args : str) -> str:
    path = os.path.join(*args)
    path = path_normpath(path)
    if NAME_FOLDER_SEP != os.path.sep:
        path = path.replace(os.path.sep, NAME_FOLDER_SEP)
    return path

def path_normpath(d:str ) -> str:
    return d.replace('\\','/')

def re_search__i(pattern : str, text: str, i : int, terror : str = '') -> str:
    try:
        m =  re.search(pattern,text)
        if m:
            return m[i]
    except:...
    return terror


def bridge(jloc : dict[str,Any]) -> None:
    import pandas as pd
    import numpy as np
    jloc['pd'] = pd
    jloc['np'] = np
    jloc['re'] = re
    jloc['datetime'] = datetime
    jloc['os'] = os
    #jloc['swe'] = tools.swe
    jloc['disp'] = disp


def disp(x : Any, max_rows : int = 5000) -> None: 
    from IPython.display import display
    import pandas as pd
    if type(x) == pd.DataFrame or type(x) == pd.Series:
        if x.shape[0] > max_rows:
            x = x.iloc[0:max_rows]

        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', None):  # more options can be specified also
            display(x) 
    else:
        display(x) 

#def reload() -> None:
#    lt_reload = []
#    for k,v in sys.modules.items():
#        if k.startswith(bindfiles.__name__):
#            lt_reload.append(v)
#            #print(k,'yes')
#
#    for m in lt_reload:
#        importlib.reload(m)

T = TypeVar('T')      # Declare type variable

def run_safe(fun : Callable[[Any],T], msg:str, ret_error: T, *arg : Any,**kwrg :Optional[Any]) -> T:
    '''ESTRUTURA PARA RODAR FUNÇÃO DENTRO DE TRY_EXCEPT'''
    try:
        return fun(*arg,**kwrg)
    except Exception as exp:
        print(f'Erro em {msg}:\n{exp}')
        return ret_error
  

def flat (lf:list[T], remove : bool = True, add_folder: bool = True) ->list[T]:
    
    #TGEN = list[dict[str,Any]]
    queue:list[tuple[list[dict[str,Any]],str]] = [( cast(list[dict[str,Any]], lf),'')]
    lr : list[dict[str,Any]] = []

    while len(queue) > 0:        
        lq, folder = queue.pop(0)
        for i in lq:
            if add_folder:
                i['folder'] = folder
            
            la = i
            if 'childs' in i: 
                subfolder = path_join(folder,i['name'])
                queue.append( ( i['childs'],subfolder) ) #List[File] = Union[List[Dfile],List[LFile]]
                if remove:
                    la = copy(i)
                    la['childs'] = []
            lr.append(la)
    return cast(list[T],lr)

def user_data(folder: str) -> str:
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['LOCALAPPDATA'], folder)
    else:  # Linux (e macOS)
        return os.path.join(os.path.expanduser('~'), '.config', folder)



'''
    #DEPRECATED

    #HELP FUNCTIONS
def str_to_t64( t:str) -> str:
    return base64.b64encode(str.encode(t)).decode('utf-8')

def t64_to_str( t64:str) ->str:
    return base64.b64decode(t64).decode('utf-8')


def file_to_file64( file:str, file64:str) ->None:
    folder,fname = os.path.split(file)
    folder64,name64 = os.path.split(file64)

    bdata : bytes = b''
    with open(file,'rb') as bfile:
        bdata = bfile.read()
    t64 = base64.b64encode(bdata).decode('utf-8')

    if not folder64:
        folder64 = folder
    with open(path_join(folder64,name64),'w') as tf:
        tf.write(t64)

def file64_to_file( file64:str, file:str) -> None:
    folder64,name64 = os.path.split(file64)
    folder,fname = os.path.split(file)
    
    t64:str = ''
    with open(file64,'r') as t64file:
        t64 = t64file.read()
    
    if not folder:
        folder = folder64
    with open(path_join(folder,name64),'wb') as tf:
        tf.write( base64.b64decode(t64) )


'''