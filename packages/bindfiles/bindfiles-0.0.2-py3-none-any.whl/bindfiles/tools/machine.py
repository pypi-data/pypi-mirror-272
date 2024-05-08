
from __future__ import annotations
import os
import typing_extensions
from typing import Union, cast, Any, Optional, TypeVar,Callable, Dict, List
from datetime import datetime, timezone
from copy import deepcopy ,copy
import shutil
import operator
#import pandas as pd
#import numpy as np
import pytz
import re	


from enum import Enum


from bindfiles.tools.search_engine import list_files, add_fields
from bindfiles.api.drive import File,  Drive
import bindfiles.api.creds as gcred
from bindfiles.tools.funcs import  path_join, path_normpath, flat

from bindfiles.tools.file_source import source, opt_list

#File = Union[DFile, LFile]
#list_file = Union[list[File], list[DFile], list[LFile]]


class Source(typing_extensions.TypedDict, total=False):
    folder: str
    folders: str



#_OPTIONS_FILE, _OPTIONS_FOLDER = ('include_file','exclude_file'),('include_folder','exclude_folder')
#_OPTIONS_DEF_TRUE = ('local_names') #dexar explícito opção para converter nomes do GDrive/Linux para formato Windows : True or False

ORPHANS = typing_extensions.Literal['left','right','both','none']
SIDE = typing_extensions.Literal['left','right']


COMPARISON = typing_extensions.Literal['DIF','MULTIPLE','ORPHAN','SAME','FOLDER'] #'FOLDER' é retorno de comparação de pasta com pasta.
KEY_HASH = typing_extensions.Literal[ 'sha256Checksum', 'md5Checksum', 'sha1Checksum' ]

FCR = tuple[str, list[File],list[File], COMPARISON] #FILE COMPARISON RESULT

class COMP_RIGOR(Enum):
    HASH = 1
    DATE_SIZE = 2
    SIZE = 3

class opt_comp(typing_extensions.TypedDict, total=False):
    tipos : list[COMPARISON]# = ['DIF','MULTIPLE','ORPHAN', 'FOLDER']  
    rigor : COMP_RIGOR #= COMP_RIGOR.HASH


#LEGADO
OPERATOR = typing_extensions.Literal['or','and']
class opt_update(typing_extensions.TypedDict, total=False):
    #side : SIDE
    orphan : ORPHANS
    newer : SIDE
    op : OPERATOR
    mirror : bool
    verbose : bool


class bind_tools:

    @staticmethod
    def print_file(lf : List[File], txt: str, n : int) -> None:
        t = "\t"
        for i in lf:
            
            print(f" {t*n} {txt} {i['folder']}.{i['name']} {i.get('modifiedTime','__')}")

    
    @staticmethod   
    def match_name(la: List[File], lb: List[File],
                fun: Callable[[str, list[File], list[File]], Any ]) -> None:
                #filter: Callable[[File], bool] = lambda f: True):
        
        '''
        1) Comparação não vai igualar quando de um lado é Google Doc, Google Sheet e do outro é .xlsx ou .docx
            mimeType:
            application/vnd.google-apps.document
            application/vnd.google-apps.spreadsheet
            ficou com diferença de 4 horas / 5 horas e poucos minutos

        2) Caracteres inválidos em nome de arquivo no Windows '&' por '_'
        '''          
        
        map_a: Dict[str, list[File]] = {}
        map_b: Dict[str, list[File]] = {}

        for fa in la:
            map_a.setdefault(path_join(fa['folder'], fa['name']), []).append( fa )
            
        for fb in lb:
            map_b.setdefault(path_join(fb['folder'], fb['name']), []).append( fb )

        for path, lta in map_a.items():
            ltb = map_b.get(path, [])        
            fun(path, lta, ltb)
            map_a[path] = lta
            map_b[path] = ltb

        for path, ltb in map_b.items():
            if not path in map_a:
                lta = []
                fun(path, lta, ltb)
                map_a[path] = lta
                map_b[path] = ltb
        
        for p in map_a.keys() | map_b.keys():
            lta,ltb = map_a[p], map_b[p]
            
            def cget(lt: list[File]) -> tuple[ list[File],bool] :
                if len(lt) == 1 and 'childs' in lt[0]:
                    return lt[0]['childs'], True
                else:
                    return [], False
            lca,ba = cget(lta)
            lcb,bb = cget(ltb)

            #if ba and bb:
            bind_tools.match_name(lca, lcb, fun)        


        la[:] = [f for lt in map_a.values() for f in lt] #lta = [f for k, lt in map_a.items() if k.startswith('A') for f in lt]
        lb[:] = [f for lt in map_b.values() for f in lt] 


    
    
    @staticmethod
    def callback_comparar(*, rigor : COMP_RIGOR = COMP_RIGOR.HASH ) -> Callable[[str, list[File],list[File]], COMPARISON]: #path, la, lb, comp
        '''
        retorna lista consolidada - por nome, padrão que tenha 1 ou 0 itens em cada lista, mas pode ocorrer mais, 
        '''
        #tipos = opt_comp.get('tipos', None ) #sem same
        #rigor = opt_comp.get('rigor',COMP_RIGOR.HASH)

        def cb_comp( path: str, la: list[File], lb: list[File]) -> COMPARISON:

            c : COMPARISON = 'DIF'
            if len(la) > 1 or len(lb) > 1:
                c = 'MULTIPLE'
                
            elif len(la) == 0 or len(lb) == 0:
                c = 'ORPHAN'

            else:
                fa, fb = la[0], lb[0]
                
                lh : list[KEY_HASH] = [ 'sha256Checksum', 'md5Checksum', 'sha1Checksum' ]
                for h in lh:
                    if h in fa and h in fb and fa[h] and fa[h] == fb[h]:
                        c = 'SAME'
                if rigor == COMP_RIGOR.DATE_SIZE:
                    if fa['size'] == fb['size'] and fa['modifiedTime'] == fb['modifiedTime']:
                        c = 'SAME'
                elif rigor == COMP_RIGOR.SIZE:
                    if fa['size'] == fb['size']:
                        c = 'SAME'


            if c != 'MULTIPLE': #sem complexidades
                
                lca : list[File] = la[0]['childs'] if len(la) == 1 and 'childs' in la[0] else []
                lcb : list[File] = lb[0]['childs'] if len(lb) == 1 and 'childs' in lb[0] else []

                if len(la) == 1 and 'childs' in la[0] and len(lb) == 1  and 'childs' in lb[0]:
                    c = 'FOLDER' #PASTA NÃO DIZ QUE É IGUAL OU DIF, DEPENDE DE CONTEÚDO
                
                #print(la[0].get('name','NAME'))
                #bind_tools.match_name( lca,lcb, cb_comp)
            return c
        
        return cb_comp  
    
    
    @staticmethod
    def comparar(la: List[File], lb: List[File], *,
                    opt_comp : opt_comp ) -> list[FCR]: #path, la, lb, comp
        '''
        retorna lista consolidada - por nome, padrão que tenha 1 ou 0 itens em cada lista, mas pode ocorrer mais, 
        '''
        ret : list[tuple[str, list[File],list[File], COMPARISON]] = []

        tipos = opt_comp.get('tipos', None)
        rigor = opt_comp.get('rigor', COMP_RIGOR.HASH )
        fget_comp = bind_tools.callback_comparar(rigor=rigor)

        def criterio( path: str, la: list[File], lb: list[File]) -> tuple[list[File], list[File]]:
            c = fget_comp(path,la,lb)
            if tipos is None or c in tipos:
                ret.append((path, la,lb, c))
            return la, lb
        bind_tools.match_name( la,lb, criterio)
        return ret    
    
    @staticmethod
    def lt_file_unpack( la:list[File], lb:list[File]) -> tuple[Optional[File],Optional[File]]:
        ''' precisa tratar antes casos dissonantes  '''
        if len(la) > 1 or len(lb) > 1:
            raise RuntimeError(f'multiple files with same name: {la[0].get("name",None) or lb[0].get("name",None)} [{len(la)}][{len(lb)}]  ')
        return la[0] if len(la) == 1 else None, lb[0] if len(lb) == 1 else None     

    
    @staticmethod
    def filter_update( *,side: Optional[SIDE] = None , newer : bool = False, orphan : bool = False,  mirror: bool = False, 
                      rigor : COMP_RIGOR = COMP_RIGOR.HASH) -> Callable[[str, list[File],list[File]],bool] :

        #['DIF','MULTIPLE','ORPHAN','SAME','FOLDER']
        fcomp = bind_tools.callback_comparar(rigor=rigor)

        def ffilter(path: str, fa: list[File], fb: list[File] ) -> bool:
            comp = fcomp(path, fa,fb)
            def finside() -> bool:                

                if comp == 'DIF':
                    if mirror:
                        return True                

                    if newer:
                        fileA, fileB = fa[0],fb[0]
                        if fileA['isfile'] and fileB['isfile']:
                            dif = ns.comp_isodate(fileA['modifiedTime'], fileB['modifiedTime'])
                            if (side == 'left' and dif == -1) or (side == 'right' and dif == 1):
                                return True
                elif comp == 'ORPHAN':
                    if mirror:
                        return True                
                    if orphan:
                        if side == 'left':
                            return len(fa) == 0
                        elif side == 'right':
                            return len(fb) == 0
                        else:
                            return True
                #elif comp == 'FOLDER':
                #    return True

                return False
            b = finside()
            #print(path,b,comp,side,len(fa), len(fb))
            return b
        return ffilter



    @staticmethod
    def update( sa:source, sb: source,
                *, verbose : bool = False, rigor : COMP_RIGOR = COMP_RIGOR.HASH ,
                side: SIDE, newer : bool = False, orphan : bool = False,  mirror: bool = False) -> list[tuple[list[File],list[File]]]:

        lt_result : list[tuple[list[File],list[File]]] = []


        update_filter = bind_tools.filter_update(side=side, newer=newer, orphan= orphan, mirror=mirror, rigor=rigor)


        s_source, s_target = sa, sb        
        if side == 'left':
            s_source, s_target = sb, sa
        
        def fun_upload(path: str, l_source:list[File], l_target:list[File]) -> None:

            la, lb = l_source, l_target
            if side == 'left':
                lb, la = l_source, l_target

            if update_filter(path, la, lb):        
                
                f_source, f_target = bind_tools.lt_file_unpack(l_source,l_target) #raise se for múltiplo

                if f_source and f_target and  (f_source['isfile'] != f_target['isfile']):
                    #corrige diferença 
                    if  mirror:
                        if verbose:
                            print(f'deleting {side}', path_join( f_source['folder'], f_source['name'])  )

                        if f_target['isfile']:
                            s_target.file_delete(f_target['id'])
                        else:
                            s_target.path_delete( path_join(f_target['folder'], f_target['name']))
                        
                        f_target = None

                if f_source:
                    if f_source['isfile']:
                        
                        if verbose:
                            print(f'updating {side}', path_join( f_source['folder'], f_source['name'])  )
                        
                        blob = s_source.get_blob(f_source['id'])
                        if f_target:
                            s_target.write_blob(f_target,blob=blob)
                        else:
                            f_target = s_target.create_file(f_source['name'],f_source['folder'],blob=blob,mimeType=f_source.get('mimeType',None))
                        f_target = s_target.update_file(f_target,source=f_source,fields='modifiedTime') #mais algum?
                    else:
                        if f_target:
                            ... #pasta igual
                        else:
                            f_target = s_target.path_makedirs( path_join(f_source['folder'],f_source['name']) )
                
                elif not f_source:
                    if f_target:
                        if mirror: #
                            if verbose:
                                print(f'deleting {side}', path_join( f_target['folder'], f_target['name'])  )

                            if f_target['isfile']:
                                s_target.file_delete(f_target['id'])
                                
                            else:
                                s_target.path_delete( path_join(f_target['folder'], f_target['name']))
                            f_target = None

                l_source[:], l_target[:] = [f_source] if f_source else [], [f_target] if f_target else [] #retorno pack
                
                la, lb = l_source, l_target
                if side == 'left':
                    lb, la = l_source, l_target
                lt_result.append((la,lb))
            
            
        bind_tools.match_name(s_source.lt_files, s_target.lt_files, fun_upload)

        return lt_result




LT_DEBUG : list[Any] = []

class bind:
    
    def __init__(self, sa: source, sb : source, opt : opt_list = {}) -> None:
        
        self._sa, self._sb = sa, sb
        self._opt : opt_list =  opt
        sa._opt = sb._opt =  opt
        
        self._sa.listar(flat=False)
        
        #print('sa',len(self._floor.sa.lt_files))
        self._sb.listar(flat=False)
        #print('sb',len(self._floor.sb.lt_files))

        #sem alguma chave necessária para comparação #key, path, file
        self._xa :list[tuple[str,str,File]] = [] 
        self._xb :list[tuple[str,str,File]] = []

        #self._result :list[pair] = self.bind__comparar()    

    @staticmethod
    def filter_inloc( lq : list[File], filter: Callable[[File],bool]) -> None:
        
        ln_file : list[File] = []

        for f in lq:
            if not filter( f ):
                continue

            if 'childs' in f:
                bind.filter_inloc(f['childs'], filter) 

            ln_file.append(f)

        lq[:] = ln_file     


    def comp_legado(self, opc : opt_comp = {}, opu : opt_update = {} ) -> list[tuple[str, list[File],list[File], COMPARISON]]: #path, la, lb, comp
        return bind_legado.comparar_legado(self._sa.lt_files, self._sb.lt_files, opt_comp=opc, opt_up= opu )

    def comparar(self, opc : opt_comp = {}) -> list[tuple[str, list[File],list[File], COMPARISON]]: #path, la, lb, comp
        return bind_tools.comparar(self._sa.lt_files, self._sb.lt_files, opt_comp=opc )

    def comp_df(self, *, side: SIDE, newer : bool = False, orphan : bool = False,  mirror: bool = False, filter : bool = True  ) ->Any: #pd.DataFrame
        import pandas as pd
            
            #opt['tipos'] =  ['DIF','MULTIPLE','ORPHAN','FOLDER','SAME']

        lr = bind_tools.comparar(self._sa.lt_files, self._sb.lt_files, opt_comp={} )        
        
        if filter:
            fr = bind_tools.filter_update(side=side, mirror=mirror, newer=newer, orphan=orphan)
            lr = [ i for i in lr if fr(i[0],i[1],i[2])]


        lt = []
        for path,la,lb,comp in lr:
            #if comp == 'FOLDER':
            #    continue
            d = { 'path': path, 'status': comp,  'mod-a': '', 'sz-a': '', 'mod-b': '', 'sz-b': ''}
            for f in la:
                d['mod-a'] = ns.isodate(f['modifiedTime']).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                d['sz-a'] =  ns.sz(f,1)
                break
            
            for f in lb:
                d['mod-b'] = ns.isodate(f['modifiedTime']).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                d['sz-b'] =  ns.sz(f,1)
                break
            lt.append(d)
        return pd.DataFrame(lt)





    def bind__update_to(self, side:SIDE, orphan:bool, newer:bool,op:Optional[OPERATOR] = None, mirror:bool = False,verbose:bool = False) -> list[Any]:
        return []

        '''
        lt_updated : list[pair] = []
        if orphan == False and newer == False:
            return lt_updated
        
        check_side:SIDE = 'right' if side == 'left' else 'left'
        fo:Optional[ORPHANS] = check_side if orphan else None
        fn:Optional[SIDE] = check_side if newer else None
        
        lt_kept : list[pair] = []

        def copy_if_applied(f: pair, keep_on_error:bool) ->bool:
            if f.pair_filtrar(orphan=fo, newer=fn, op=op):
                #se achar aqui no filtro, faz uma cópia
                try:
                    pn = self._floor.floor_copy(f,side=side)
                    if verbose:
                        print(f'updating {side}',f.pair_path_name())
                    lt_updated.append(f)
                except Exception as e:
                    if verbose:
                        print('Erro:',e)
                    if keep_on_error:
                        lt_kept.append(f)
                    raise
                return True
            return False


        for files in self._result:
            if copy_if_applied(files,keep_on_error=True):
                ...
                
            elif mirror:
                #continue
                msg = f'deleting {side}',files.pair_path_name() #depois que apaga files não mantém vínculo com o nome.
                if self._floor.floor_delete(files,side=side) and verbose:
                    if not copy_if_applied(files,keep_on_error=False): #não manteve - Já teve parte apagada
                        print(*msg)
                    
            else:
                lt_kept.append(files)
                
        self._result = lt_kept
        return lt_updated
        '''

    
    def update_right(self, *, orphan:bool = True, newer:bool = True, verbose:bool = False) -> list[tuple[list[File],list[File]]]:
        return bind_tools.update(self._sa, self._sb, verbose=verbose, side='right',newer=newer, orphan= orphan)
    
    def update_left(self, *, orphan:bool = True, newer:bool = True, verbose:bool = False) -> list[tuple[list[File],list[File]]]:
        return bind_tools.update(self._sa, self._sb, verbose=verbose, side='left',newer=newer, orphan= orphan)

    def mirror_right(self,verbose:bool = False) -> list[tuple[list[File],list[File]]]:
        return bind_tools.update(self._sa, self._sb, verbose=verbose, side='right',mirror=True)
    
    def mirror_left(self ,verbose:bool = False) -> list[tuple[list[File],list[File]]]:
        return bind_tools.update(self._sa, self._sb, verbose=verbose, side='left',mirror=True)


    
    def _result_side(self, side:SIDE, orphan:bool, newer:bool,isfile:Optional[bool]) -> list[File]:
        lr : list[File] = []
        if orphan == False and newer == False:
            return lr
        
        fo:Optional[ORPHANS] = side if orphan else None
        fn:Optional[SIDE] = side if newer else None


        '''
        
        for files in self._result:
            if files.pair_filtrar(orphan=fo, newer=fn, op='or'):
                if side == 'left' and files.fa:
                    if bind.bind_static__file_add(isfile, files.fa):
                        lr.append(files.fa)
                elif side == 'right' and files.fb:
                    if bind.bind_static__file_add(isfile, files.fb):
                        lr.append(files.fb)
        '''
        return lr
    
    def result_right(self,orphan:bool, newer:bool, isfile:Optional[bool] = None) -> list[File]:
        return bind._result_side(self,'right',orphan=orphan,newer=newer,isfile=isfile)
        #return self._result_side('left',orphan=orphan,newer=newer,op=op)
    
    def result_left(self,orphan:bool, newer:bool, isfile:Optional[bool] = None) -> list[File]:
        return bind._result_side(self,'left',orphan=orphan,newer=newer,isfile=isfile)
        ##return self._result_side('right',orphan=orphan,newer=newer,op=op)




class ns:
    @staticmethod
    def isodate(dtime: str) -> datetime:
        #return datetime.fromisoformat(dtime[0:19]) #até segundos #v1 
        return datetime.fromisoformat(dtime[0:19]).replace(tzinfo=timezone.utc) #v3

    
    @staticmethod
    def isodate_gdrive_to_local(file:File) -> datetime:
        #v1 return ns.isodate(file) - (datetime.now().utcnow() - datetime.now()) #v1
        
        #v2   Supondo que ns.isodate(file) retorna um datetime em UTC
        #file_utc_datetime = ns.isodate(file)
        #   Calcular a diferença entre a hora atual UTC e a hora atual local
        #utc_offset = datetime.now(timezone.utc) - datetime.now()
        #   Ajustar a data/hora do arquivo para o horário local
        #local_datetime = file_utc_datetime - utc_offset
        #return local_datetime
        
        file_utc_datetime = ns.isodate(file['modifiedTime']) #v3
        # Converte a hora UTC para a hora local do sistema
        local_datetime = file_utc_datetime.astimezone()
        return local_datetime

    @staticmethod
    def str_isodate(file:Optional[File]) -> str:
        if file is None:
            return ''
        dt = datetime.fromisoformat(file['modifiedTime'][0:19]) #até segundos
        return dt.strftime('%Y-%m-%d %H:%M') 
    
    @staticmethod
    def time_brazil() -> datetime:  #USEI NO ASTRODATA
        tz = pytz.timezone('America/Sao_Paulo')
        format = "%Y-%m-%d %H:%M:%S.%f"
        return datetime.strptime(datetime.now(tz=tz).strftime(format),format) #evita problema no DataFrame - não salva Excel se tiver timezone    

    @staticmethod
    def sz(file:Optional[File], exp:int = 0) -> str:
        if file is None:
            return ''
        elif  file.get('childs',None) or file.get('isfile',False):  #diretório
            return '-'
        return str(int(int(file.get('size',0)) / (1024)** exp))
    
    @staticmethod
    def comp_isodate(tdt1:str,tdt2:str) -> int:
        tdt1, tdt2 = tdt1[0:19], tdt2[0:19] #até segundos
        if tdt1 == tdt2:
            return 0
        if datetime.fromisoformat(tdt1) < datetime.fromisoformat(tdt2):
            return -1
        else:
            return 1        



#class floor:
        

#print('upload')        
#path_name = path_join(spath,name)
#ocal_path = sa.local_path(path_name)
#folder_id = sb.id(spath)

#if fa and sb.drive:
#    if 'childs' in fa:
#        new_drive_folder = sb.drive.create_folder(folder_id,fa['name'])
#        sb._drive__dic_id[path_name] = new_drive_folder['id']
#        return cast(File, new_drive_folder)
#    else:
#        fn =sb.drive.upload_file(folder_id,local_path,fields='id,name,md5Checksum') #PRECISA DE MIMETYPE?
#        LT_DEBUG.append(fn)
#        if fn and fb:
#            sb.drive.delete_file(fb['id'])
#        return cast(File,fn)
#else:
#    raise RuntimeError('')


#@staticmethod
#def floor_download(ls:source,lf:Optional[File], ds:source,df:Optional[File],name:str, spath:str ) -> File:
#        
#    path_name = path_join(spath,name)
#    local_path = ls.local_path(path_name)
#    
#    if df and ds.drive:
#        if 'childs' in df:
#            if not os.path.isdir(local_path):
#                os.makedirs(local_path)
#        else:
#            try:
#                ds.drive.downlad_file(df['id'], local_path, ns.isodate_gdrive_to_local(df))
#            except:
#                raise RuntimeError(f'Não foi possível fazer download de {df["name"]} {df["id"]}')
#                ... #posso listar, mover - passar função onde resolvo o que fazer
#        return cast(File,{}) #aprimorar se necessário
#    else:
#        raise RuntimeError('')
    



    
'''
def floor_copy(self, p:pair, side:SIDE) -> pair:
    #sa,sb = (self.sa, self.sb) if right else (self.sb,self.sa)
    sa,sb = self.sa, self.sb
    if sa._source_check('local') and sb._source_check('local'):
        pA = sa.local_path(p.pair_path_name())
        pB = sb.local_path(p.pair_path_name())

        if side == 'right' and p.fa:
            if 'childs' in p.fa:
                os.makedirs(pB)
            else:
                shutil.copyfile(pA,pB)
        elif side == 'left' and p.fb:
            if 'childs' in p.fb:
                os.makedirs(pA)
            else:
                shutil.copyfile(pB,pA)
        return p
    elif sa._source_check('local') and sb._source_check('gdrive'):
        if side == 'right':
            p.fb = floor._floor_upload(sa,p.fa,sb,p.fb,p.pair_name(),p.spath)
        elif side == 'left':
            p.fa = floor.floor_download(sa,p.fa,sb,p.fb,p.pair_name(),p.spath)
        else:
            raise RuntimeError()
        return p
    elif sa._source_check('gdrive') and sb._source_check('local'):
        if side == 'left':
            p.fa = floor._floor_upload(sb,p.fb,sa,p.fa,p.pair_name(),p.spath)
        elif side == 'right':
            p.fb = floor.floor_download(sb,p.fb,sa,p.fa,p.pair_name(),p.spath)
        else:
            raise RuntimeError()
        return p
    elif sa._source_check('gdrive') and sb._source_check('gdrive'):
        pA = sa.id(p.spath)
        pB = sb.id(p.spath)
        ...  
        return p               
    else:
        raise RuntimeError()
'''





class bind_legado:    




    @staticmethod
    def comparar_legado(la: List[File], lb: List[File], *,                    
                    opt_comp : opt_comp, opt_up : opt_update ) -> list[FCR]: #path, la, lb, comp
        '''
        retorna lista consolidada - por nome, padrão que tenha 1 ou 0 itens em cada lista, mas pode ocorrer mais, 
        '''
        ret : list[FCR] = []

        tipos = opt_comp.get('tipos', ['DIF','MULTIPLE','ORPHAN','FOLDER'] ) #sem same
        rigor = opt_comp.get('rigor',COMP_RIGOR.HASH)

        op_filter = bind_legado.filter_legado(opt= opt_up)

        def criterio( path: str, lf_source: list[File], lf_target: list[File]) -> tuple[list[File], list[File]]:
            
            badd = True
            c : COMPARISON = 'DIF'
            if len(lf_source) > 1 or len(lf_target) > 1:
                c = 'MULTIPLE'
                
            elif len(lf_source) == 0 or len(lf_target) == 0:
                c = 'ORPHAN'
                badd = op_filter(lf_source[0], None) if len(lf_source) else op_filter(None, lf_target[0])

            else:
                fa, fb = lf_source[0], lf_target[0]
                
                badd = op_filter(fa,fb)
                
                lh : list[KEY_HASH] = [ 'sha256Checksum', 'md5Checksum', 'sha1Checksum' ]
                for h in lh:
                    if h in fa and h in fb and fa[h] and fa[h] == fb[h]:
                        c = 'SAME'
                if rigor == COMP_RIGOR.DATE_SIZE:
                    if fa['size'] == fb['size'] and fa['modifiedTime'] == fb['modifiedTime']:
                        c = 'SAME'
                elif rigor == COMP_RIGOR.SIZE:
                    if fa['size'] == fb['size']:
                        c = 'SAME'


            if c != 'MULTIPLE': #sem complexidades
                
                lca : list[File] = lf_source[0]['childs'] if len(lf_source) == 1 and 'childs' in lf_source[0] else []
                lcb : list[File] = lf_target[0]['childs'] if len(lf_target) == 1 and 'childs' in lf_target[0] else []

                if len(lf_source) == 1 and 'childs' in lf_source[0] and len(lf_target) == 1  and 'childs' in lf_target[0]:
                    c = 'FOLDER' #PASTA NÃO DIZ QUE É IGUAL OU DIF, DEPENDE DE CONTEÚDO

                if badd and c in tipos:
                    ret.append((path, lf_source,lf_target, c))
                
                #propagar subpastas
                bind_tools.match_name( lca,lcb, criterio)
            
            else:
                if badd and c in tipos:
                    ret.append((path, lf_source,lf_target, c))

            
            return lf_source, lf_target    
        
        bind_tools.match_name( la,lb, criterio)
        return ret

    @staticmethod
    def filter_legado(opt : opt_update ) -> Callable[ [Optional[File], Optional[File]] , bool ]:
        
        newer = opt.get('newer', None)
        orphan = opt.get('orphan',None)
        top = opt.get('op',None)
        #side = opt.get('side','left')

        #se já tem opção de lateralidade está impícito um OR ao escolher newer (orfão não é mais ou menos recente)
        #caso contrário o newer vai restringir
        op_ = operator.and_ if (orphan == 'both' or orphan == 'none') else operator.or_
        if top:
            op_ = operator.or_ if (top == 'or') else operator.and_


        def run_filter(fs: Optional[File], ft: Optional[File] ) -> bool:
            #if side == 'left':
            #    ft,fs = fs,ft
            
            bo:bool = True
            if orphan:
                if orphan == 'left'and ((fs is None) or (ft is not None)):
                    bo = False
                elif orphan == 'right' and ((ft is None) or (fs is not None)):
                    bo = False
                elif orphan == 'both' and ((fs is None) == (ft is None)):
                    bo = False                
                elif orphan == 'none' and ((fs is None) != (ft is None)):
                    bo = False

            
            bn: bool = True
            if newer:
                if ((fs is not None) and (ft is not None)):
                    
                    dif = ns.comp_isodate(fs['modifiedTime'], ft['modifiedTime'] )
                    if newer == 'left' and dif != 1:
                        bn = False
                    elif newer == 'right' and dif != -1:
                        bn = False
                else:
                    bn = False            

            
            ret = False
            if orphan and newer:
                ret =  op_(bo,bn) 
            elif orphan:
                ret =  bo
            elif newer:
                ret =  bn

            #print( fs['name'] if fs else '', ft['name'] if ft else '', op_, ret, bo,bn)
            return ret
            
        return run_filter
    
    @staticmethod
    def update_legado( sa:source, sb: source, opt : opt_update ) -> None: #Callable[ [str, list[File], list[File]], None]:

        verbose = opt.get('verbose',False)
        op_filter = bind_legado.filter_legado(opt)
        mirror = opt.get('mirror',False)

        s_source, s_target = sa, sb
        
        side = opt.get('side','right')
        if side == 'left':
            s_source, s_target = sb, sa
        
        def fun_upload(path: str, l_source:list[File], l_target:list[File]) -> tuple[list[File],list[File]]:

            f_source, f_target = bind_tools.lt_file_unpack(l_source,l_target) #raise se for múltiplo
            
            fa, fb = f_source, f_target
            if side == 'left':
                fb, fa = f_source, f_target
            
            if mirror or op_filter(fa, fb):        
                
                if f_source and f_target and  (f_source['isfile'] != f_target['isfile']):
                    #corrige diferença 
                    if  mirror:
                        if f_target['isfile']:
                            s_target.file_delete(f_target['id'])
                        else:
                            s_target.path_delete( path_join(f_target['folder'], f_target['name']))
                        f_target = None

                if f_source:
                    if f_source['isfile']:
                        if verbose:
                            print(f'updating {side}', path_join( f_source['folder'], f_source['name'])  )
                        
                        blob = s_source.get_blob(f_source['id'])
                        if f_target:
                            s_target.write_blob(f_target,blob=blob)
                        else:
                            f_target = s_target.create_file(f_source['name'],f_source['folder'],blob=blob,mimeType=f_source.get('mimeType',None) )
                        f_target = s_target.update_file(f_target,source=f_source,fields='modifiedTime') #mais algum?
                    else:
                        if f_target:
                            ... #pasta igual
                        else:
                            f_target = s_target.path_makedirs( path_join(f_source['folder'],f_source['name']) )
                
                elif not f_source:
                    if f_target:
                        if mirror: #
                            if f_target['isfile']:
                                s_target.file_delete(f_target['id'])
                                
                            else:
                                s_target.path_delete( path_join(f_target['folder'], f_target['name']))
                            f_target = None

                l_source[:], l_target[:] = [f_source] if f_source else [], [f_target] if f_target else [] #retorno pack
            
            return l_source, l_target
        
        bind_tools.match_name(s_source.lt_files, s_target.lt_files, fun_upload)

    
        


