import pandas as pd
import my_libs.ociteb_utils  as ou
import my_libs.ociteb_context as oc;
import re

class Wos:
 
    def __init__(self):
        self.dic_addresses_records={}
        self.array_synonyms_pais={}

    def sgi_process(self,source_string_sgi):
        regex  = r'sgi [0-9]{4}|SGI [0-9]{4}|SGI[0-9]{4}|SGI: [0-9]{4}|SGI-[0-9]{4}|SGI. [0-9]{4}|SGI\n[0-9]{4}|SGI [0-9]{3}-|SGI.  [0-9]{4}|SGI No [0-9]{4}|SGI SEGUN|SGI:[0-9]{4}|SGI N° [0-9]{4}|SGI NO [0-9]{4}|SGI - [0-9]{4}|SGI Project [0-9]{4}'
        _sgi = ou.String_utils.search_string_pattern(regex,source_string_sgi)
        return _sgi

    def get_list_emails(self,source_string_email):
        record_list = source_string_email.split(";")
        return record_list;
    
    def addresses_process(self,source_string,array_synonyms_pais):
        self.array_synonyms_pais=array_synonyms_pais
        self.dic_addresses_records={}
        record_list = source_string.split("[")
        tam_list = len(record_list)
        key_ord=1;
        for i in range(1,tam_list):
            position=ou.String_utils.search_index_char(record_list[i],']')
            authors_data  = record_list[i][0:position]
            filation_data = record_list[i][position+2:]           
            key = str(key_ord);
            self.dic_addresses_records[key]=self.addresses_reccord_process(authors_data,filation_data)
            key_ord+=1
        return(self.dic_addresses_records)

    def addresses_reccord_process(self,authors_data,filation_data):
        list_filation_data = filation_data.split(", ")
        dict_filations = {
            'universidad'   : False,
            'facultad'      : False,
            'escuela'       : False,
            'grupo'         : False,
            'research site' : False,
            'ciudad'        : False,
            'departamento'  : False,
            'pais'          : False,
            'direccion'     : False,
        }
        addresses_record = {
            'autores'       : [],
            'is_uptc'       : 'NO',
            'universidad'   : 'NE',
            'facultad'      : 'NE',
            'escuela'       : 'NE',
            'grupo'         : 'NE',
            'research site' : 'NE',
            'ciudad'        : 'NE',
            'departamento'  : 'NE',
            'pais'          : 'NE',
            'direccion'     : 'NE',
            'otros'         : [],
        }
        addresses_record['autores'] = authors_data.split("; ")

        for name in oc.array_uptc_names:
            if(name in filation_data.upper()):
               addresses_record['is_uptc'] = 'SI'

        for filiation in list_filation_data:
            if re.findall(' \d\d\d\d\d', filiation):
                    addresses_record['ciudad']  = filiation
                    dict_filations['ciudad']    = True  
            else:
                for key_filiation in dict_filations:
                    match=False    
                    if dict_filations[key_filiation] == False:
                        array_synonyms = self.select_synonym(key_filiation)
                        addresses_record[key_filiation],match = self.set_filation_item(filiation,array_synonyms)
                        if match:
                            dict_filations[key_filiation] = match
                            break
                if not match:
                    addresses_record['otros'].append(filiation)
                
        return(addresses_record)

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
             return self.array_synonyms_pais
        elif key_filiation=='direccion':
             return oc.array_synonyms_direccion
        elif key_filiation=='research site':
             return oc.array_synonyms_research_site
        return None
  

    def set_filation_item(self,item,array_synonyms):
        # quita puntuación y pasa a mayusculas
        item_clean = re.sub(r'[^\w\s]','',item.upper())
        item_clean = ou.String_utils.replace_accents(item_clean)
        for sub_item in array_synonyms:
            if item_clean.rstrip() == sub_item.rstrip():
                return item, True
        else:
            array_item = item_clean.split()
            for sub_item in array_synonyms:
                for word_item in array_item:
                    if sub_item == word_item:
                        return item, True
        return 'NE', False
    
    def email_process(self,person, list_email):
        separadores = "[^a-zA-Z]+"
        list_parts_person = re.split(separadores, person)
        for mail in list_email:
            contador = 0
            for part in list_parts_person:
                if part.lower() in mail.lower():
                    contador = contador + 1
            if contador > 1:
                return mail
        return "";
