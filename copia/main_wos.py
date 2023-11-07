# -*- coding: UTF8 -*-
import my_libs.ociteb_dataframe as od
import pandas as pd
import my_libs.ociteb_wos  as wos
import my_libs.ociteb_context as oc
import datetime
import requests


def get_countries():
    SOURCE_PATH = 'data/origin/'
    SOURCE_FILE_MAIN = 'paises.xlsx'

    sheet_main  = od.Sheet_dataframe(SOURCE_PATH + SOURCE_FILE_MAIN)
    series_select_list = ['NOMBRE', 'NAME']
    sheet_main.generate_new_dataframe(series_select_list)
    new_df=sheet_main.get_new_dataframe()
    return new_df['NOMBRE'], new_df['NAME']


SOURCE_PATH = 'data/source/'
SOURCE_FILE_MAIN = 'SOURCE_WS.xlsx'
TARGET_PATH = 'data/target/' 
TARGET_FILE_MAIN = 'wos_autor_2023.xlsx'

sheet_main  = od.Sheet_dataframe(SOURCE_PATH + SOURCE_FILE_MAIN)

series_select_list = [  'Addresses', 'Affiliations', 'Article Title', 'Author Full Names', 'Author Keywords', 
                        'Authors', 'Date of Export', 'Document Type', 'DOI', 'DOI Link', 'eISSN', 'Email Addresses', 
                        'Funding Orgs', 'Funding Name Preferred','Funding Text', 'ISBN','ISSN', 'Keywords Plus', 
                        'Language','ORCIDs', 'Publication Year', 'Publisher City', 'Research Areas', 'Source Title', 
                        'Web of Science Index', 'WoS Categories']

sheet_main.generate_new_dataframe(series_select_list)

new_df=sheet_main.get_new_dataframe()


wos_columns_list = [    'code','author code' ,'author','university','uptc','faculty','school','group','city','department','country',
                        'address','research site','others','email', 'SGI-Funding Orgs', 'SGI-Funding Name Preferred','SGI-Funding Text',
                        'Addresses','Affiliations', 'Article Title','Article Date' ,'Author Full Names', 'Author Keywords','Authors', 
                        'Date of Export', 'Document Type', 'DOI', 'DOI Link', 'eISSN', 'Email Addresses','Funding Name Preferred', 
                        'Funding Orgs','Funding Text', 'ISBN','ISSN', 'Keywords Plus', 'Language','ORCIDs', 'Publication Year', 
                        'Publisher City','Research Areas', 'Source Title', 'Web of Science Index', 'WoS Categories']

obj_wos = wos.Wos()

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

consecutivo_articulo=0
df_wos_by_author = pd.DataFrame(columns=wos_columns_list)
array_synonyms_pais_nombre, array_synonyms_pais_name  =  get_countries()
array_synonyms_pais = pd.concat([array_synonyms_pais_name,array_synonyms_pais_nombre])

for i in range(0,len(new_df)):
# for i in range(60,70):

    source_string=new_df['Addresses'][i]
    source_emails=new_df['Email Addresses'][i]

    dic_addresses = obj_wos.addresses_process(source_string,array_synonyms_pais)
    
    if pd.isna(source_emails):
         list_emails=[]
    else:
        print(source_emails)
        list_emails   = obj_wos.email_addresses_process(source_emails)
 
    SGI_Org  = str(new_df['Funding Orgs'][i])
    SGI_Preferred  = str(new_df['Funding Name Preferred'][i])
    SGI_Text  = str(new_df['Funding Text'][i])
   
    SGI_Funding_Orgs = obj_wos.sgi_process(SGI_Org)
    SGI_Funding_Name_Preferred = obj_wos.sgi_process(SGI_Preferred)
    SGI_Funding_Text = obj_wos.sgi_process(SGI_Text)

    print(i+1)
    print(new_df['Article Title'][i])
    consecutivo_autor=0
    is_cooperation=False

    for item in dic_addresses.items():
        in_uptc   = False
        in_others = False
        print(item[1]['universidad'].upper())
        for name in oc.array_uptc_names:
            if name in item[1]['universidad'].upper():
                in_uptc = True
            else:
                in_others = True

        print("---------------")
        list_autores =  item[1]['autores']
        code='wos-'+ year + '-' + str(i+1) 

        for autor in list_autores:
            list_columns_data = []

            email_adresses = 'NE'
            if consecutivo_autor < len(list_emails):
                email_adresses = list_emails[consecutivo_autor]
            
            consecutivo_autor+=1
            author_code=code+ '-' + str(consecutivo_autor)
            url_doi="NE"
            fecha_articulo_string ="NE"
            if str(new_df['DOI'][i]).strip()=="" or pd.isna(new_df['DOI'][i]):
                fecha_articulo_string="NE"
            else:
                url_doi="https://doi.org/api/handles/" + new_df['DOI'][i] + "?type=HS_ADMIN"
                res = requests.get(url_doi)
                if(res.status_code==200):
                    json = res.json()
                    dic_values = json["values"][0]
                    fecha_articulo_string = dic_values["timestamp"]
                    fecha_articulo_string = fecha_articulo_string[0:10]
                else:
                    fecha_articulo_string="NP"
            
            list_columns_data.append(code)
            list_columns_data.append(author_code)
            list_columns_data.append(autor)   
            list_columns_data.append(item[1]['universidad'])
            list_columns_data.append(item[1]['is_uptc'])
            list_columns_data.append(item[1]['facultad'])
            list_columns_data.append(item[1]['escuela'])
            list_columns_data.append(item[1]['grupo'])
            list_columns_data.append(item[1]['ciudad'])
            list_columns_data.append(item[1]['departamento'])
            list_columns_data.append(item[1]['pais'])
            list_columns_data.append(item[1]['direccion'])

            list_columns_data.append(item[1]['research site'])
            list_columns_data.append(item[1]['otros'])

            list_columns_data.append(email_adresses.lstrip())

            list_columns_data.append(SGI_Funding_Orgs)
            list_columns_data.append(SGI_Funding_Name_Preferred)
            list_columns_data.append(SGI_Funding_Text)

            list_columns_data.append(new_df['Addresses'][i])
            list_columns_data.append(new_df['Affiliations'][i])
            list_columns_data.append(new_df['Article Title'][i])
            list_columns_data.append(fecha_articulo_string)
            list_columns_data.append(new_df['Author Full Names'][i])
            list_columns_data.append(new_df['Author Keywords'][i])
            list_columns_data.append(new_df['Authors'][i])
            list_columns_data.append(new_df['Date of Export'][i])

            list_columns_data.append(new_df['Document Type'][i])
            list_columns_data.append(new_df['DOI'][i])
            list_columns_data.append(new_df['DOI Link'][i])
            list_columns_data.append(new_df['eISSN'][i])
            list_columns_data.append(new_df['Email Addresses'][i])
            list_columns_data.append(new_df['Funding Name Preferred'][i])
            list_columns_data.append(new_df['Funding Orgs'][i])

            list_columns_data.append(new_df['Funding Text'][i])
            list_columns_data.append(new_df['ISBN'][i])
            list_columns_data.append(new_df['ISSN'][i])
            list_columns_data.append(new_df['Keywords Plus'][i])
            list_columns_data.append(new_df['Language'][i])
            list_columns_data.append(new_df['ORCIDs'][i])
            list_columns_data.append(new_df['Publication Year'][i])
            list_columns_data.append(new_df['Publisher City'][i])

            list_columns_data.append(new_df['Research Areas'][i])
            list_columns_data.append(new_df['Source Title'][i])
            list_columns_data.append(new_df['Web of Science Index'][i])
            list_columns_data.append(new_df['WoS Categories'][i])

            df_wos_by_author.loc[len(df_wos_by_author.index)] = list_columns_data
           

df_wos_by_author.to_excel(TARGET_PATH + TARGET_FILE_MAIN)
print('OK')