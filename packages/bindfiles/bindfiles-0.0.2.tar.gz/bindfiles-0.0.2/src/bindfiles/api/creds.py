#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

'''
https://console.cloud.google.com/
CRIEI PROJETO
'''


from __future__ import annotations

import base64
import os
import pickle
import json
import requests
import re
import typing_extensions


from typing import Any, cast, Union, Callable, Optional, TypedDict, List
from datetime import datetime
from bindfiles.tools import funcs

class OathDict(TypedDict):
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: List[str]
    expiry: Optional[datetime]


from google.auth.transport.requests import Request as Transport_Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials #novo



DEFAULT_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://mail.google.com/', #'https://www.googleapis.com/auth/gmail.send', 
    'https://www.googleapis.com/auth/drive', 
    'https://www.googleapis.com/auth/photoslibrary',
    'https://www.googleapis.com/auth/drive.appdata',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/documents']
#https://developers.google.com/identity/protocols/oauth2/scopes?hl=pt-br


OATH_SOURCE = typing_extensions.Literal['', 'url','py'] #'' preferência para web, conforme webapp

class WEBAPP_STORGE:
    FILENAME = r'Scripts\bindfiles\url.txt'

    def __init__(self,  cred : Any = 0 , id : str = '') -> None:
        
        '''
        cred : int if key at webapp storage else the key values / incluir recurso armazenar no webapp        
        '''
        self.url = ''
        if id.startswith('http'):
            self.url = id
        elif id:
            self.url = f'https://script.google.com/macros/s/{id}/exec'
        else:
            self.url = open( funcs.user_data(self.FILENAME),"r").read().strip()
        
        self.cred = cred #para caso de ter que refazer 
        self.token_oath : Optional[Union[Credentials,str]] = None

    def _cred(self) -> Any:  #i in case of mutliple credentials at webapp
        if type(self.cred) == int:
            return  self._post(f'={self.cred}', None).json() #{'a':23}
        return self.cred
    
    def _post(self,path: str, json : Optional[dict[str,str]]) -> requests.Response:
        #print(f'post path={path} json={json}')
        
        try:
            url = f'{self.url}?cred{path}'
            #print('request', url)
            resp = requests.post(url,json=json, timeout=10) #f'{self._URL}{path}         

            if len(resp.text) and resp.text[0] == '<': #== '<' código html
                from IPython.display import display
                from IPython.core.display import HTML
                #print(resp.text)
                display(HTML(resp.text))
                
                raise RuntimeError('retorno inválido')
            return resp
        except Exception as e:
            print(f'erro ao acessar url {url}\n{e}')
            raise e


    def load(self, key:str,*, scopes: Optional[list[str]] = None, refaz : bool = False , oath_source : OATH_SOURCE = '' ) -> Any:
        #https://console.cloud.google.com/apis/credentials #?project=pythonlocal-1597696138984


        def ler() -> Union[Credentials,str]: 
            r = self._post('',json={'get': oath_source,'ac':key})  #'get':'py' or 'url'  
            try:
                token_data = r.json()
                
                return Credentials(token=token_data['token'],
                        refresh_token=token_data['refresh_token'],
                        token_uri=token_data['token_uri'],
                        client_id=token_data['client_id'],
                        client_secret=token_data['client_secret'],
                        scopes=token_data['scopes'])
            except Exception as e:
                if r.text:
                    return r.text #token string do GoogleAppScript
                raise e
        try:
            if refaz == False:
                if not self.token_oath: # or not self.token_oath.valid:
                    self.token_oath = ler()

    
                if self.token_oath and isinstance(self.token_oath, Credentials) and self.token_oath.expired:
                    if self.token_oath.refresh_token:
                        self.token_oath.refresh(Transport_Request())
                    else:
                        refaz = True
            if refaz or not self.token_oath:
                if scopes is None:
                    scopes = DEFAULT_SCOPES   
                config = self._cred()
                
                flow = InstalledAppFlow.from_client_config(config, scopes=scopes)  
                cred_token : Credentials= flow.run_local_server(port=0)
                if cred_token: #atualizar se refez
                    self._post('', json= {'store':'','ac':key, 'py': cred_token.to_json()})
                    self.token_oath = cred_token
                raise RuntimeError('')
            
            return self.token_oath
    
        except Exception as e:
            print(e)
            raise e
        
    def store_url(self, key:str, value:str) -> None:
        #para webapp com storage
        self._post('', json= {'store':'','ac': key, 'url': value})
        self.token_oath = None
        _ = self.load(key)

    def store_py(self, key:str, value:Credentials) -> None:
        #para webapp com storage
        self._post('', json= {'store':'','ac': key, 'py': value.to_json()})
        self.token_oath = None
        _ = self.load(key)

    
    def test(self , key:str) -> None:
        k = self.load(key)
        print(k)



#IMPLEMENTAÇÃO LOCAL
def load(key:str, *,  scopes : Optional[list[str]] = None, refaz : bool = False,  oath_source : OATH_SOURCE = '', id : str = '') -> Any: #para descrição deixar isso em C++, nome do módulo ou onde pega carona.
    #arg = locals() #parâmetros dessa função
    mk = WEBAPP_STORGE(id=id)
    return mk.load(key=key,scopes=scopes, refaz=refaz, oath_source= oath_source)

def store(key:str, value: Union[str, Credentials], *, cred : Any = 0, id: str = '') -> None:
    mk = WEBAPP_STORGE(id = id, cred=cred)
    if type(value) == str:
        return mk.store_url( key=key, value=value ) #**locals()
    elif type(value) == Credentials:
        return mk.store_py( key=key, value=value)
