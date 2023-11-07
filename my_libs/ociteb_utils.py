import pandas as pd
import re

class String_utils:

    @staticmethod
    def replace_accents(source_string):
        a,b = 'áéíóúüÁÉÍÓÚ','aeiouuAEIOU'
        trans = str.maketrans(a,b)
        return(source_string.translate(trans))
    
    @staticmethod
    def remove_null_spaces(source, msg_null='Nulo', msg_empty='Vacio'):
        if (pd.isnull(source)):
            cell = msg_null
        else:
            cell = source.strip()
            if cell == '':
                cell = msg_empty
        return cell

    @staticmethod
    def remove_inter_spaces(source_string):
        target_string = ""
        for i in range(len(source_string)+1):
            if source_string[i-1:i]!=" ":
                target_string = target_string + source_string[i-1:i]
            else:    
                if source_string[i-2:i-1]!=" ":
                    target_string = target_string + source_string[i-1:i]
        return (target_string)

    @staticmethod
    def remove_first_space(source_string):
        return (source_string.lstrip())


    @staticmethod
    def remove_last_space(source_string):
        return (source_string.rstrip())

    @staticmethod
    def  search_index_char(source_string,char):
        index = source_string.find(char)
        return index

    @staticmethod
    def  search_string_pattern(regex, source_string):
       return re.findall(regex, source_string)
    
class Serie_utils:
    
    @staticmethod
    def modify_serie_with_criteria_list(df,serie,criteria,msg=''):
        try:
            nrows = df.shape[0]
            for indice in range(nrows):
                if('REMOVE_FIRST_SPACES' in criteria):
                    df.at[indice, serie]= String_utils.remove_first_spaces(df.iloc[indice][serie], msg)
                if('REMOVE_NULL_SPACES' in criteria):
                    df.at[indice, serie]= String_utils.remove_null_spaces(df.iloc[indice][serie], msg)
                if('REMOVE_INTER_SPACES' in criteria):
                    df.at[indice, serie]= String_utils.remove_inter_spaces(df.iloc[indice][serie])
                if('REPLACE_ACCENTS' in criteria):
                    df.at[indice, serie]= String_utils.replace_accents(df.iloc[indice][serie])
                if('TO_UPPER' in criteria):
                    df.at[indice, serie]=df.iloc[indice][serie].upper()
                if('TO_LOWER' in criteria):
                    df.at[indice, serie]=df.iloc[indice][serie].lower()
                if('TO_CAPITALIZE' in criteria):
                    df.at[indice, serie]=df.iloc[indice][serie].capitalize()
                if('TO_TITLE' in criteria):
                    df.at[indice, serie]=df.iloc[indice][serie].title()
        except Exception as e:
            print('error: ' + type(e).__name__)

