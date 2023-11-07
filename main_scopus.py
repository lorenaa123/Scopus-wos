# -*- coding: UTF8 -*-
import  my_libs.ociteb_utils  as ou
import pandas as pd
import  my_libs.ociteb_dataframe  as od
import  my_libs.ociteb_context as oc;
import  my_libs.ociteb_scopus  as scopus
import datetime
import requests
import re
from dateutil.parser import parse

SOURCE_PATH = 'data/source/'
SOURCE_FILE_MAIN = '20230606SCOPUSTOTAL.xlsx'
TARGET_PATH = 'data/target/' 
TARGET_FILE_MAIN = 'scopus_autor_2023.xlsx'

sheet_main  = od.Sheet_dataframe(SOURCE_PATH + SOURCE_FILE_MAIN)

series_select_list = [  'Authors with affiliations', 'Author(s) ID','Affiliations','Author Keywords', 'Authors', 'Authors with affiliations',
                        'Conference date','Conference name','Correspondence Address','Document Type','DOI','Funding Details',
                        'Funding Text 1','Funding Text 2','Funding Text 3', 'Index Keywords','ISBN','ISSN',
                        'Language of Original Document','Link','Publisher','Source title','Title','Year']

scopus_columns_list = [ 'code','author code', 'author','Author ID','university','uptc','faculty','school','group','city','department','country','address','others',
                        'SGI-Funding Orgs', 'SGI-Funding Name Preferred','SGI-Funding Text', 'Conference date',  'ISSN',  'Email Addresses',
                        'Addresses','Affiliations', 'Article Title','Article Date' ,'Author Full Names', 'Author Keywords','Authors', 'Date of Export', 
                        'Document Type', 'DOI', 'DOI Link','Funding Name Preferred', 'Funding Orgs', 
                        'Funding Text', 'ISBN','ISSN', 'Keywords Plus', 'Language','ORCIDs', 'Publication Year', 'Publisher City', 
                        'Research Areas', 'Source Title', 'Web of Science Index', 'WoS Categories']

sheet_main.generate_new_dataframe(series_select_list)

new_df=sheet_main.get_new_dataframe()

obj_scopus = scopus.Scopus()

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

consecutivo_articulo=0
df_scopus_by_author = pd.DataFrame(columns=scopus_columns_list)

def procesa_correo(persona, cadena_lista_correos):
    apellido = persona.split(',')[0].strip()
    lista_correos = re.findall(r'\S+@\S+', cadena_lista_correos)
    for correo in lista_correos:
        if "@uptc.edu.co" not in correo:
            continue
        if apellido.lower() in correo.lower():
            return correo.strip()
    return "NE"


#for i in range(0,len(new_df)):
for i in range(0,150):

    source_string=new_df['Authors with affiliations'][i]

    dic_authors_with_affiliations=obj_scopus.authors_with_affiliations_process(source_string)
    SGI_Org  = str(new_df['Funding Details'][i])
    SGI_Preferred  = str(new_df['Funding Text 1'][i])
    SGI_Text  = str(new_df['Funding Text 2'][i])
    SGI_Funding_Orgs = obj_scopus.sgi_process(SGI_Org)
    SGI_Funding_Name_Preferred = obj_scopus.sgi_process(SGI_Preferred)
    SGI_Funding_Text = obj_scopus.sgi_process(SGI_Text)

    has_uptc_author = False
 
    for author in dic_authors_with_affiliations:
        for item in dic_authors_with_affiliations.items():
            if item[1]['is_uptc'] =="SI":
                has_uptc_author = True
                break
    
    if has_uptc_author:
        consecutivo_articulo+=1
        if(len(dic_authors_with_affiliations)>0):
            new_record_scopus=[]
            consecutivo_autor=0
            for item in dic_authors_with_affiliations.items():
                

                consecutivo_autor+=1
                list_columns_data = []
                
                code='scopus-'+ year + '-' + str(consecutivo_articulo) 
                codeAutor = code + '-' + str(consecutivo_autor)
                

                print(code)

                url_doi="NE"
                fecha_articulo_string ="NE"
                if str(new_df['DOI'][i]).strip()=="" or pd.isna(new_df['DOI'][i]):
                    fecha_articulo_string="NP"
                else:
                    try:
                        url_doi="https://doi.org/api/handles/" + new_df['DOI'][i] + "?type=HS_ADMIN"
                        res = requests.get(url_doi)
                        if(res.status_code==200):
                            json = res.json()
                            dic_values = json["values"][0]
                            fecha_articulo_string = dic_values["timestamp"]
                            fecha_articulo_string = fecha_articulo_string[0:10]
                        else:
                            fecha_articulo_string = "NP"
                    except requests.exceptions.RequestException:
                        fecha_articulo_string = "No se pudo consultar la URL"
                    


                newIssn = ""
                
                if str(new_df['ISSN'][i]).strip()=="" or pd.isna(new_df['ISSN'][i]):
                    newIssn ='NE'
                else: 
                    issn_sin_guiones = new_df['ISSN'][i].replace('-', '')
                    issn_con_guiones = '{}-{}'.format(issn_sin_guiones[:4], issn_sin_guiones[4:])
                    newIssn = issn_con_guiones


                fecha_original = new_df['Conference date'][i]

                if str(fecha_original).strip() == "" or pd.isna(fecha_original):
                        dateConference = 'NE'
                else:
                    fecha_inicio, _, fecha_fin = fecha_original.partition(" through ")

                    try:
                        fecha_inicio = parse(fecha_inicio).strftime("%d/%m/%y")
                        fecha_fin = parse(fecha_fin).strftime("%d/%m/%y")
                        dateConference = f"{fecha_inicio} al {fecha_fin}"
                    except ValueError:
                        dateConference = 'Formato de fecha incorrecto'
                
                try:
                    author_ids = new_df['Author(s) ID'][i].strip().split(';')
                    if consecutivo_autor <= len(author_ids):
                        id_author = author_ids[consecutivo_autor - 1]
                    else:
                        print(f"Consecutivo de autor {consecutivo_autor} fuera de rango.")
                except KeyError:
                    print("'Author(s) ID' no encontrada en el DataFrame.")
                except IndexError:
                    print(f"Índice {i} fuera de rango para 'Author(s) ID'.")


    
                


                

                list_columns_data.append(code)
                list_columns_data.append(codeAutor)
                list_columns_data.append(item[1]['autor'])
                list_columns_data.append(id_author)
                list_columns_data.append(item[1]['universidad'])
                list_columns_data.append(item[1]['is_uptc'])
                list_columns_data.append(item[1]['facultad'])
                list_columns_data.append(item[1]['escuela'])
                list_columns_data.append(item[1]['grupo'])
                list_columns_data.append(item[1]['ciudad'])
                list_columns_data.append(item[1]['departamento'])
                list_columns_data.append(item[1]['pais'])
                list_columns_data.append(item[1]['direccion'])
                list_columns_data.append(item[1]['otros'])
                list_columns_data.append(SGI_Funding_Orgs)
                list_columns_data.append(SGI_Funding_Name_Preferred)
                list_columns_data.append(SGI_Funding_Text)
                list_columns_data.append(dateConference)
                list_columns_data.append(newIssn)

                autor = item[1]['autor'] 
                posicion = list_columns_data.index(autor) 
                mails = new_df['Correspondence Address'][i]
                if str(mails).strip() == "" or pd.isna(mails):
                    mailAssigment = 'NE'
                else:
                    mailAssigment = procesa_correo(autor, mails)

                    
                list_columns_data.append(mailAssigment)
                list_columns_data.append(new_df['Authors with affiliations'][i])
                list_columns_data.append(new_df['Affiliations'][i])
                list_columns_data.append(new_df['Title'][i])
                list_columns_data.append('NE')
                list_columns_data.append(new_df['Authors'][i])
                list_columns_data.append(new_df['Author Keywords'][i])
                
                list_columns_data.append('NE')
                list_columns_data.append(fecha_articulo_string)
                list_columns_data.append(new_df['Document Type'][i])
                list_columns_data.append(new_df['DOI'][i])
                list_columns_data.append(new_df['Link'][i])
                list_columns_data.append('NE')
                list_columns_data.append(new_df['Funding Details'][i])
                list_columns_data.append(new_df['Funding Text 1'][i])
                list_columns_data.append(new_df['Funding Text 2'][i])
                list_columns_data.append(new_df['ISBN'][i])
                list_columns_data.append(new_df['Index Keywords'][i])
                list_columns_data.append(new_df['Language of Original Document'][i])
                list_columns_data.append('NE')
                list_columns_data.append(new_df['Year'][i])
                list_columns_data.append('NE')
                list_columns_data.append('NE')
                list_columns_data.append(new_df['Source title'][i])
                list_columns_data.append(new_df['Publisher'][i])
                list_columns_data.append('NE')
                df_scopus_by_author.loc[len(df_scopus_by_author.index)] = list_columns_data

df_scopus_by_author.to_excel(TARGET_PATH + TARGET_FILE_MAIN)
print('OK')