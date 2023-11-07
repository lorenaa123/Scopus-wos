import pandas as pd
import my_libs.ociteb_utils  as ou
import my_libs.ociteb_context as oc
import re


class Scopus:
 
    def __init__(self):
        self.dic_addresses_records={}

    def sgi_process(self,source_string_sgi):
        regex  = r'sgi [0-9]{4}|SGI [0-9]{4}|SGI[0-9]{4}|SGI: [0-9]{4}|SGI-[0-9]{4}|SGI. [0-9]{4}|SGI\n[0-9]{4}|SGI [0-9]{3}-|SGI.  [0-9]{4}|SGI No [0-9]{4}|SGI SEGUN|SGI:[0-9]{4}|SGI N° [0-9]{4}|SGI NO [0-9]{4}|SGI - [0-9]{4}|SGI Project [0-9]{4}'
        _sgi = ou.String_utils.search_string_pattern(regex,source_string_sgi)
        return _sgi
    
    # def is_uptc(self,source_string):
    #     if isinstance(source_string, str):
    #         source_list = source_string.split(";")
    #         self.dic_addresses_records={}
    #         key_ord=1;
    #         for record in source_list:
    #             for synonym in oc.array_uptc_names:
    #                 if synonym.upper() in record.upper():
    #                     position=ou.String_utils.search_index_char(record,'., ')
    #                     author = record[0:position]
    #                     filation_data = record[position+2:] 
    #                     filation_uptc_list.append(self.addresses_reccord_process(author,filation_data))  
    #                     key = str(key_ord);
    #                     self.dic_addresses_records[key]=self.addresses_reccord_process(author,filation_data)
    #                     key_ord+=1
    #     else:
    #         print("error")     
    #     return(self.dic_addresses_records)


    #-------------------------------
        
    # def authors_with_affiliations_process(self,source_string):
    #     if isinstance(source_string, str):
    #         source_list = source_string.split(";")
    #         self.dic_addresses_records={}
    #         key_ord=1;
    #         for record in source_list:
    #             new_record = ou.String_utils.replace_accents(record)
    #             position=ou.String_utils.search_index_char(new_record,'., ')
    #             author = new_record[0:position]
    #             filation_data = new_record[position+2:] 
    #             key = str(key_ord)
    #             self.dic_addresses_records[key]=self.addresses_reccord_process(author,filation_data)
    #             key_ord+=1
    #     else:
    #         print("error")     
    #     return(self.dic_addresses_records)

    def authors_with_affiliations_process(self, source_string):
        if isinstance(source_string, str):
            source_list = source_string.split(";")
            self.dic_addresses_records = {}
            key_ord = 1
            for record in source_list:
                new_record = ou.String_utils.replace_accents(record)
                position = ou.String_utils.search_index_char(new_record, '., ')
                author = new_record[0:position]
                if len(author) < 100:
                    filation_data = new_record[position + 2:]
                    key = str(key_ord)
                    self.dic_addresses_records[key] = self.addresses_reccord_process(author, filation_data)
                    key_ord += 1
                else:
                    print(f"Author too long: {author}")
            return self.dic_addresses_records
        else:
            print("error")





    def addresses_reccord_process(self,author,filation_data):
       
        list_filation_data = filation_data.split(", ")
        dict_filations = {
            'universidad'   : False,
            'facultad'      : False,
            'escuela'       : False,
            'grupo'         : False,
            'ciudad'        : False,
            'departamento'  : False,
            'pais'          : False,
            'direccion'     : False
        }
        authors_with_affiliations_record = {
            'autor'         : 'NE',
            'universidad'   : 'NE',
            'is_uptc'       : 'NO',
            'facultad'      : 'NE',
            'escuela'       : 'NE',
            'grupo'         : 'NE',
            'ciudad'        : 'NE',
            'departamento'  : 'NE',
            'pais'          : 'NE',
            'direccion'     : 'NE',
            'otros'         : [],
        }
        authors_with_affiliations_record['autor'] = author

        for name in oc.array_uptc_names:
            if(name in filation_data.upper()):
               authors_with_affiliations_record['is_uptc'] = 'SI'

        for filiation in list_filation_data:  
            for key_filiation in dict_filations:
                match=False    
                if dict_filations[key_filiation] == False:
                    array_synonyms = self.select_synonym(key_filiation)
                    authors_with_affiliations_record[key_filiation],match = self.set_filation_item(filiation,array_synonyms)
                    if match:
                        dict_filations[key_filiation] = match
                        break
            if not match:
                authors_with_affiliations_record['otros'].append(filiation)
                
        return(authors_with_affiliations_record)

    def select_synonym(self,key_filiation):
        if key_filiation=='universidad':
            return oc.array_synonyms_universidad
        elif key_filiation=='facultad':
            return oc.array_synonyms_facultad
        elif key_filiation=='escuela':
            return oc.array_synonyms_escuela
        elif key_filiation=='grupo':
            return oc.array_synonyms_grupo
        elif key_filiation=='ciudad':
            return oc.array_synonyms_ciudad
        elif key_filiation=='departamento':
            return oc.array_synonyms_departamento
        elif key_filiation=='pais':
            return oc.array_synonyms_pais
        elif key_filiation=='direccion':
            return oc.array_synonyms_direccion
        return None
        
    def set_filation_item(self,item,array_synonyms):
            for sub_item in array_synonyms:
                if sub_item.upper() in item.upper():
                    return item, True
            return 'NE', False
        
