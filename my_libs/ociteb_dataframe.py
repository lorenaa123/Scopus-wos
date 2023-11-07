import pandas as pd
import  my_libs.ociteb_utils  as ou

class Sheet_dataframe:
 
    def __init__(self, file,sheet_name=''):
        if sheet_name=='':
            self.df = pd.read_excel(file)
        else:
            self.df = pd.read_excel(file, sheet_name )
        self._new_df = pd.DataFrame()
        self._series_names_list =  self.df.columns.tolist()
        self._series_select_list = []
  
    def get_all_name_series(self):
        return self._series_names_list

    def generate_new_dataframe(self, series_select_list, new_names = []):
       indice = 0
       for serie in series_select_list:
        if len(new_names) == 0:
            self._new_df[serie] = self.df[serie]
        else:
            self._new_df[new_names[indice]] = self.df[serie]
            indice+=1

    def add_new_column(self, col_name,data=[]):
            self._new_df[col_name] = pd.Series(data)
            
    def get_new_dataframe(self):
        return self._new_df 
    
    def modify_serie_with_criteria_list(self,SERIE,CRITERIA,MSG=''):
        ou.Serie_utils.modify_serie_with_criteria_list(self._new_df,SERIE,CRITERIA,MSG)

class Sheet_merge:
    def __init__(self, df_main, df_child, key):
        self._df_main = df_main
        self._df_child = df_child
        self._key = key
        self._list_filter=None
        self._df_merge=None

    def generate_merge_dataframe(self):
        self._list_filter = self._df_main[self._key].tolist()
        self._df_merge = self._df_child[self._df_child[self._key].isin(self._list_filter)] 
        self._df_merge = pd.merge(self._df_merge,self._df_main,on=self._key)
    
    def get_df_merge(self):
        return  self._df_merge 
