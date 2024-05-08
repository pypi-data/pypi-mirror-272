from __future__ import annotations


import os.path
#import numpy as np

from googleapiclient.discovery import build
from typing import Any, cast, Union, Callable, Optional

import builtins

from bindfiles.gclient.sheets_v4 import  ( Request as sheet_request, BatchUpdateSpreadsheetRequest, 
            BatchUpdateSpreadsheetResponse, GridProperties, GridRange, CellData, Color,
            ValueRange, UpdateValuesResponse, AppendValuesResponse, BatchGetValuesResponse,
            )


import typing
import typing_extensions

#https://www.datacamp.com/tutorial/inner-classes-python VER Inner

import re
#import pandas as pd


BASE_ZERO = False 

#https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.html
class Sheet_Requests():
    def __init__(self, sheet_parent : Sheet) -> None:
        self.sheets = sheet_parent

    def run(self, lt :list[sheet_request] ) -> BatchUpdateSpreadsheetResponse:
        if self.sheets.id is None:
            raise RuntimeError()

        if len(lt) ==0:
            raise RuntimeError('Nenhum Request na lista')
        body : BatchUpdateSpreadsheetRequest = { "requests":lt } 


        try:
            
            response = self.sheets.service.spreadsheets().batchUpdate(spreadsheetId= self.sheets.id, body=body).execute()
            return response
        except Exception as e: 
            lt_metodos = [list(i.keys())[0] for i in lt]
            raise RuntimeError(f'error on any of "{",".join(lt_metodos)}"\n{e}\n\n {body}') from e


    def grid_update(  self, rowCount :Optional[int] = None, columnCount :Optional[int] = None, 
                    frozenRowCount :Optional[int] = None, frozenColumnCount :Optional[int] = None, hideGridlines :Optional[bool] = None,
                    rowGroupControlAfter :Optional[bool] = None, columnGroupControlAfter :Optional[bool] = None) -> sheet_request:
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#updatesheetpropertiesrequest
        
        PAR : list[str] = ['columnGroupControlAfter','frozenColumnCount','frozenRowCount','hideGridlines','rowCount','rowGroupControlAfter']
        gp = { k:v for k,v in locals().items() if k in PAR and v is not None }
        fields = ','.join(['gridProperties.' + k for k in gp])

        if len(gp) == 0:
            raise RuntimeError("Nenhum item passado para atualizar")

        g : sheet_request =  { "updateSheetProperties": { #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#sheetproperties
                        "properties": {  #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#GridProperties
                            "sheetId": self.sheets.gid,
                            "gridProperties": cast( GridProperties, gp )
                        },"fields": fields } }
        return g
        

    
    def border(self, li_b1 :int, ci:int ,lf:Optional[int] = None,cf:Optional[int]=None,
                style:str = 'SOLID', borders:list[str]=['bottom'], color:list[float]=[0.6,0.6,0.6] ) -> sheet_request:
        '''
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#updatebordersrequest
        
        dicBorder ['top','bottom','left','right','innerHorizontal','innerVertical'] 
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#Border
        '''
        
        req : sheet_request = {} #'updateBorders': dicBorder}
        req['updateBorders'] = {'range':self.sheets.GridRange(li_b1,ci,lf,cf)}

        rgbcolor =  { "red": color[0], "green": color[1], "blue": color[2] } #, "alpha": 1 if len(color) <4 else color[3]

        CELLBORDER = ['top','bottom','left','right','innerHorizontal','innerVertical']
        for key in borders: # req['updateBorders'].__dict__['__optional_keys__']: 
            icheck = CELLBORDER.index(key) #garangir
            req['updateBorders'][key] = { "style": style, 'color': rgbcolor } # type: ignore
        return req                    
    
    
    def hyperlink(self, rowIndex:int, colIndex:int, face:Union[str,int,float], hyperlink:str, base0:bool = BASE_ZERO )  -> sheet_request:
        
        text = f'"{face}"'
        if type(face) == float:
            text = f'{face}'.replace('.',',') #BRASIL
        
        return {"updateCells": {
            "rows": [
                {"values": [{ "userEnteredValue": { "formulaValue": f'=HYPERLINK("{hyperlink}";{text})'} }]}
                ],
            "fields": "userEnteredValue",
            "start": {
                "sheetId": self.sheets.gid,
                "rowIndex": rowIndex-1,
                "columnIndex": colIndex-1
            }
        }}
        #f = lambda x: f'https://drive.google.com/file/d/{x}/view?usp=drivesdk'
        #f = lambda x: f'https://drive.google.com/uc?id={x}&export=download'

    
    
    def filter_remove(self) -> sheet_request:
        return { "clearBasicFilter": {"sheetId": self.sheets.gid }} 

    def filter_add(self, li : int, ci : int, lf : Optional[int], cf : Optional[int], base0 :bool = BASE_ZERO ) -> sheet_request:
        return {'setBasicFilter': { "filter": {
            "range": self.sheets.GridRange(li=li,ci=ci,lf=lf,cf=cf,base0=base0)
            #",sortSpecs": [ { object (SortSpec)}] #",criteria": { integer: { object (FilterCriteria) },...} #",filterSpecs": [{ object (FilterSpec) }]
            } }
        }
    def cell_numberFormat(self, li : int, ci : int, lf : Optional[int], cf : Optional[int], type : str, format : str, base0 :bool = BASE_ZERO) -> sheet_request: #numberformat - renomear
        FORMAT_TYPE :list[str] = [ "NUMBER_FORMAT_TYPE_UNSPECIFIED", "TEXT", "NUMBER", "PERCENT", "CURRENCY", "DATE", "TIME", "DATE_TIME", "SCIENTIFIC", ]
        icheck = FORMAT_TYPE.index(type)

        return {'repeatCell': {
            "range": self.sheets.GridRange(li=li,ci=ci,lf=lf,cf=cf,base0=base0),
            "cell": { #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#CellData
                "userEnteredFormat": {  #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#CellFormat
                        "numberFormat": { #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#NumberFormat
                            "type": type, # type: ignore
                            "pattern": format #https://developers.google.com/sheets/api/guides/formats
                        }
                    }
                },
            "fields": "userEnteredFormat.numberFormat"
            }
        }
        

    def sortRange(self, li : int, ci : int,  cindex:int , asc:bool = True, lf : Optional[int] = None, cf : Optional[int] = None, base0 :bool = BASE_ZERO ) -> sheet_request:
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#SortRangeRequest
        #lt = [ go.sheets.request.sortRange(li+1,ci= ci,cindex= ci+1, asc= True), go.sheets.request.sortRange(li+1,ci= ci,cindex= ci, asc= False)]
        #go.sheets.request.run(lt)
        return  {'sortRange': {
            "range": self.sheets.GridRange(li=li,ci=ci,lf=lf,cf=cf,base0=base0),
            "sortSpecs": [{  "dimensionIndex" : cindex - (0 if base0 else 1),
                            "sortOrder" : 'ASCENDING' if asc else 'DESCENDING' } ]} }

    def InsertDimension(self,li:int, row:bool = True, qt:int = 1, before:bool = False) -> sheet_request:
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#InsertDimensionRequest
        if before:
            li-=1
        return { 'insertDimension' : {
            'range' : { "sheetId": self.sheets.gid,
                "dimension": 'ROWS' if row else 'COLUMNS' ,
                "startIndex": int(li),
                "endIndex": int(li + qt)
            },
            'inheritFromBefore' : before }}

    def DeleteDimension(self,li:int, row:bool = True, qt:int = 1) -> sheet_request:
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#deletedimensionrequest
        li = li-1 #de base1 para base0
        return { 'deleteDimension' : {
            'range' : { "sheetId": self.sheets.gid,
                "dimension": 'ROWS' if row else 'COLUMNS' ,
                "startIndex": int(li),# int(li),
                "endIndex": int(li+qt), #int(li + qt)
            },}}

    def repeatcell(self,gridrange: GridRange, fieldMask: str, celldata: Any ) -> sheet_request:
        dic_celldata : dict[str,Any] = {}; dc = dic_celldata
        t = fieldMask.split('.')
        for n,i in enumerate(t):
            if n+1==len(t):
                dc[i]=celldata
            else:
                dc[i]={}
                dc = dc[i]
        
        return  {'repeatCell': {
            "range": gridrange,
            "cell": dic_celldata, #type: ignore      #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#CellData
            "fields": fieldMask #"userEnteredFormat.numberFormat"
            }
        }

    def BackgroundColor(self, li:int, ci:int, 
                        lf:Optional[int] = None, cf:Optional[int] = None,
                        color:Optional[Color] = None) -> sheet_request:
        return self.repeatcell(
            self.sheets.GridRange(li,ci,lf,cf), 'userEnteredFormat.backgroundColor', color)

    def fontSize(self, li:int, ci:int, size:int,
                 lf:Optional[int] = None, cf:Optional[int] = None) -> sheet_request:
        return self.repeatcell(
            self.sheets.GridRange(li,ci,lf,cf), 'userEnteredFormat.textFormat.fontSize', size)

    def filterView_add(self, li:int, ci:int, title: str,
                        lf:Optional[int] = None, cf:Optional[int] = None) -> sheet_request:
        return {'addFilterView': { "filter": {
            #"filterViewId": integer,
            "title": title,
            "range": self.sheets.GridRange(li,ci,lf,cf)
            #"namedRangeId": string
            #",sortSpecs": [ { object (SortSpec)}]
            #",criteria": { integer: { object (FilterCriteria) },...}
            #",filterSpecs": [{ object (FilterSpec) }]
            } }
        }        
    
    def request_conditional_format(self, li:int, ci:int,
                            lf:Optional[int] = None, cf:Optional[int] = None ) -> sheet_request:
        raise RuntimeError()
        return {}
        '''
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#conditionalformatrule
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#BooleanRule
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#BooleanCondition
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#ConditionType
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#ConditionValue
        '''
    #FIM DOS GOOGLE SHEETS - REQUESTS



class Sheet():

    ''' 
    refresh    
    https://stackoverflow.com/questions/45801313/remove-only-formatting-on-a-cell-range-selection-with-google-spreadsheet-api

    batch update    
    https://stackoverflow.com/questions/41986898/google-sheets-api-python-clear-sheet

    '''            
    
    
    def __init__(self, creds : Any) -> None:
        
        self.creds : Any
        self.id : str
        self.gid : int
        self.request = Sheet_Requests(self)
        self.service = build('sheets', 'v4', credentials= creds)

    def id_guid_from_link(self, link : str) -> None:
        #self.id, self.gid = None, None
        self.id, self.gid = re.findall('/d/(.*)/.*?gid=(\d*)',link)[0]            

    def sheet_ci_li_cf_from_range(self,range : str) -> tuple[str,int,int,int]:
        tup = re.findall("'(.*?)'!([A-Z]+)(\d+):([A-Z]+)",range.upper())[0]            
        return tup[0], self.iColuna(tup[1]),int(tup[2]),self.iColuna(tup[3])


    def GridRange(self, li:int, ci:int, lf :Optional[int] = None, cf:Optional[int] = None, base0: bool = BASE_ZERO) -> GridRange:
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#GridRange
        
        #li = int(li); ci = int(ci)
        gr : GridRange = {
            "sheetId": self.gid, 
            "startRowIndex": int(li) - (0 if base0 else 1),            
            "startColumnIndex": int(ci) - (0 if base0 else 1),
        }  
        if lf: #'endRowIndex': lf) if lf else None, #'endColumnIndex': int(cf) if cf else None 
            gr['endRowIndex'] = int(lf) 
        if cf:
            gr['endColumnIndex'] = int(cf) # if cf else None
        return gr
    
    
    def iColuna(self,txt:str)->int:
        txt = txt.upper()
        v: Callable[[str],int]  = lambda x: ord(x) - ord('A')+1
        if len(txt) == 1:
            return v(txt)
        elif len(txt) == 2:
            i,j = v(txt[0]),v(txt[1])
            return 26 + (i-1)*26 + j
        elif len(txt) == 3:
            i,j,k = v(txt[0]),v(txt[1]),v(txt[2])
            return 702 + (i-1)*26**2 + (j-1)*26 + k 
        raise RuntimeError('Calcula até 3 dígitos')   


    def tColuna(self, lcol :int) ->str:
        l_contar_digitos = 0
        ldigitos = 0
        while (l_contar_digitos < lcol):
            ldigitos+=1
            l_contar_digitos +=  26**ldigitos
            

        ldigito_menos1 = 0
        l_ultimo_dig_menos1 = 0
        while (ldigito_menos1 < (ldigitos - 1)):
            ldigito_menos1+=1
            l_ultimo_dig_menos1 = l_ultimo_dig_menos1 + 26** ldigito_menos1
        lrest = lcol - l_ultimo_dig_menos1 - 1

        ldigito = ldigitos
        lw = []
        while (ldigito > 0):
            ldigito-=1
            lpow =  26**ldigito
            ldiv = lrest //lpow
            resto = lrest % lpow
            lrest = lrest - resto
            #tc[lw] = (wchar_t)((long)t1 + ldiv.quot);
            lw.append(chr(ord('A')+ldiv))
            lrest = resto
        return ''.join(lw)                
        
    def address(self, st_name:str, lin_i:int, lin_f:int, col_i:int, col_f:int) -> str :
        return st_name + '!' + self.tColuna(col_i) + str(lin_i) + ':' + self.tColuna(col_f) + str(lin_f)

    def update(self, range:str, values: list[list[float]]) -> UpdateValuesResponse:
        responseDateTimeRenderOption: list[str] = ["SERIAL_NUMBER", "FORMATTED_STRING"]
        responseValueRenderOption: list[str] = ["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"]
        valueInputOption: list[str] = ["INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED"]

        body : ValueRange = {'majorDimension': 'ROWS','values': values}
        
        sheet = self.service.spreadsheets() # Call the Sheets API
        result = sheet.values().update(spreadsheetId=self.id, range=range,
            valueInputOption='USER_ENTERED', body=body).execute()
        return result

    def append(self, range:str, values: list[list[float]]) -> AppendValuesResponse:
            #nan = None
            bdy : ValueRange = {'majorDimension': 'ROWS','values':values}
            
            sheet = self.service.spreadsheets() # Call the Sheets API
            #valueInputOption = RAW|USER_ENTERED, insertDataOption = OVERWRITE|INSERT_ROWS, range=linha de alguma planilha
            result = sheet.values().append(spreadsheetId= self.id, range=range,
                valueInputOption='RAW',insertDataOption = 'INSERT_ROWS', body=bdy).execute()
            return result
    
    def append_row(self, range:str,  lt : list[list[float]] ) -> None:
        
        vals = self.service.spreadsheets().values()
        bdy : ValueRange = {'majorDimension': 'ROWS','values': lt }
        
        request = vals.append(spreadsheetId= self.id, range= range, valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body= bdy)
        response = request.execute()
    
    def update_df(self, st_name:str, li:int, ci:int, dfo: Any, header :bool = True ) ->None:
        import pandas as pd
        df = cast(pd.DataFrame,dfo).copy()
        for i in df.columns:
            t=str(df[i].dtype)
            if re.search('date|time',t)!=None:
                df[i] = df[i].fillna('')
                df[i] = df[i].astype('str')        
        df.fillna('',inplace = True)

        if header:
            self.update(self.address(st_name, li,li,ci, ci + df.shape[1]-1), [list(df.columns)])
            li += 1
        if df.shape[0]>0:
            dlt = []
            for rw in  df.itertuples():
                lt = [ rw[i+1] for i in range(df.shape[1])] #0 é o index
                dlt.append(lt)
            self.update(self.address(st_name,li,li+df.shape[0]-1,ci, ci + df.shape[1]-1), dlt)

    def update2_df(self,st_name : str, li:int, ci:int, df:Any,
                    grid:dict[str,Any] = {}, 
                    col_df_extra:int = 0, col_extra:int = 0, row_extra:int = 0) -> None:
        
        import pandas as pd
        d = cast(pd.DataFrame,df)
        
        lt : list[sheet_request] = [self.request.filter_remove()]
        lf = li+ d.shape[0] #tem cabeçalho
        cf = ci + d.shape[1]-1
        
        lt.append( self.request.grid_update( rowCount = lf + row_extra,
                                            columnCount = cf + col_df_extra + col_extra ,
                                            frozenRowCount=0,
                                            frozenColumnCount=0) )
        self.request.run(lt)
        
        trg_clear = self.address(st_name,li,lf,ci,cf)     
        self.clear(trg_clear) #limpar para garantir dados        
        
        self.update_df(st_name,li,ci,d, header=True)

        lt = [ self.request.grid_update(frozenRowCount=li, **grid),
        self.request.filter_add(li,ci,lf,cf+ col_df_extra)]
        self.request.run(lt)



    def clear(self, range:str) ->None:
        try:
            request = self.service.spreadsheets().values().clear(spreadsheetId=self.id, range=range) #, body=clear_values_request_body)
            response = request.execute()
            #print(response)
        except:
            print('error on clear')
            
        #https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.values.html#clear
        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear

    def values_get(self, range:str) -> ValueRange:

        #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
        #https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.html#get
        
        
        request = self.service.spreadsheets().values().get(spreadsheetId=self.id, range=range)
        response = request.execute() #, includeGridData= True
        return response
        
    
    #lin, col base0
    def values_df(self, range:str, ib0:int = 0,  lt_fields:Optional[list[str]] = None, l1_head:bool = True) -> Any:  
        '''                
        '''
        import pandas as pd
        import numpy as np
        
        resp_val = self.values_get(range)  
        values = resp_val['values']

        if l1_head:
            if lt_fields is None:
                lt_fields = cast(list[str], values[ib0].copy())
            else:
                raise ValueError('Passar lista ou usar lina1 como cabeçalho')
        
        if lt_fields is None:
            raise ValueError("lt_fields must be specified if l1_head is false.")
        
        lhead = ib0 +  (1 if l1_head else 0)
        
        qt_fields = len(lt_fields)                
        ltc: list[list[float]] = [ [] for c in lt_fields]

        for n,lt in enumerate(values): # result['values']):
            if n < lhead: 
                continue #cabeçalho
            
            lt_i = len(lt)
            for c in builtins.range(qt_fields):
                if c < lt_i:
                    ltc[c].append(lt[c])
                else:
                    ltc[c].append(np.nan)
                
        dic = { tit:ltc[c] for c,tit in enumerate(lt_fields)} #título coluna: lista com valores
        return pd.DataFrame(dic)
    
    #def grid_update(self, **kwarg):
    #    lt = [self.request.grid_update(**kwarg)]
    #    self.request.run(lt)


