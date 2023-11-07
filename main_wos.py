# -*- coding: UTF8 -*-
import my_libs.ociteb_dataframe as od
import pandas as pd
import my_libs.ociteb_wos  as wos
import my_libs.ociteb_context as oc
import datetime
import requests
import re


def get_countries():
    SOURCE_PATH = 'data/origin/'
    SOURCE_FILE_MAIN = 'paises.xlsx'

    sheet_main  = od.Sheet_dataframe(SOURCE_PATH + SOURCE_FILE_MAIN)
    series_select_list = ['NOMBRE', 'NAME']
    sheet_main.generate_new_dataframe(series_select_list)
    new_df=sheet_main.get_new_dataframe()
    return new_df['NOMBRE'], new_df['NAME']


SOURCE_PATH = 'data/source/'
SOURCE_FILE_MAIN = '20230606 WOS TOTAL.xlsx'
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

def procesa_correo(persona, cadena_lista_correos):
    separadores = "[^a-zA-Z]+"
    apellido = persona.split(',')[1].strip()
    lista_palabras = re.split(separadores, apellido)
    lista_correos = cadena_lista_correos.split(';')
    for correo in lista_correos:
        if "@uptc.edu.co" not in correo:
            continue
        contador = 0
        for palabra in lista_palabras:
            if palabra.lower() in correo.lower():
                contador += 1
        if contador >= 1:
            return correo
    return "NE"


consecutivo_articulo=0
df_wos_by_author = pd.DataFrame(columns=wos_columns_list)
array_synonyms_pais_nombre, array_synonyms_pais_name  =  get_countries()
array_synonyms_pais = pd.concat([array_synonyms_pais_name,array_synonyms_pais_nombre])

for i in range(0,len(new_df)):
#for i in range(0,20):

    source_string=new_df['Addresses'][i]
    source_emails=new_df['Email Addresses'][i]

    dic_addresses = obj_wos.addresses_process(source_string,array_synonyms_pais)
    
    SGI_Org  = str(new_df['Funding Orgs'][i])
    SGI_Preferred  = str(new_df['Funding Name Preferred'][i])
    SGI_Text  = str(new_df['Funding Text'][i])
   
    SGI_Funding_Orgs = obj_wos.sgi_process(SGI_Org)
    SGI_Funding_Name_Preferred = obj_wos.sgi_process(SGI_Preferred)
    SGI_Funding_Text = obj_wos.sgi_process(SGI_Text)

    print(i+1)
    consecutivo_autor=0
    is_cooperation=False

    list_emails=[]
    if pd.isna(source_emails):
         list_emails=[]
    else:
        list_emails   = obj_wos.get_list_emails(source_emails)

    has_uptc_author = False

    for author in dic_addresses:
        for item in dic_addresses.items():
            if item[1]['is_uptc'] =="SI":
                has_uptc_author = True
                break
    
    if has_uptc_author:
        for item in dic_addresses.items():

            list_autores =  item[1]['autores']
            code='wos-'+ year + '-' + str(i+1) 

            for autor in list_autores:
                list_columns_data = []

                email_adresses = 'NE'
                if consecutivo_autor < len(list_emails):
                    email_adresses = obj_wos.email_process(autor, list_emails)
                
                consecutivo_autor+=1
                author_code=code+ '-' + str(consecutivo_autor)
                url_doi = "NE"
                fecha_articulo_string = "NE"

                if str(new_df['DOI'][i]).strip() == "" or pd.isna(new_df['DOI'][i]):
                    fecha_articulo_string = "NE"
                else:
                    try:
                        url_doi = "https://doi.org/api/handles/" + new_df['DOI'][i] + "?type=HS_ADMIN"
                        res = requests.get(url_doi)
                        if res.status_code == 200:
                            json = res.json()
                            dic_values = json["values"][0]
                            fecha_articulo_string = dic_values["timestamp"]
                            fecha_articulo_string = fecha_articulo_string[0:10]
                        else:
                            fecha_articulo_string = "NP"
                    except requests.exceptions.RequestException:
                        fecha_articulo_string = "No se pudo consultar la URL"
                                
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

                # print(email_adresses)
                # list_columns_data.append(email_adresses.lstrip())

                # obtener el nombre del autor
                try:
                    posicion = list_columns_data.index(autor)
                    mails = new_df['Email Addresses'][i]
                    if str(mails).strip() == "" or pd.isna(mails):
                        mailAssigment = 'NE'
                    else:
                        mailAssigment = procesa_correo(autor, mails)
                except ValueError:
                    mainAssigment ="NA"
                except IndexError:
                    mainAssigment ="NA"
                

                list_columns_data.append(mailAssigment)
                # list_columns_data.append(email_adresses)

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