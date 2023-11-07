# -*- coding: UTF8 -*-
import  my_libs.ociteb_utils  as ou
import pandas as pd
import  my_libs.ociteb_dataframe  as od
import  my_libs.ociteb_context as oc;
import  my_libs.ociteb_scopus  as scopus
import datetime
import requests

SOURCE_PATH = 'data/source/'
SOURCE_FILE_MAIN = 'SCOPUS 2022.xlsx'
TARGET_PATH = 'data/target/' 
TARGET_FILE_MAIN = 'scopus_autor_2023.xlsx'


sheet_main  = od.Sheet_dataframe(SOURCE_PATH + SOURCE_FILE_MAIN)


series_select_list = [  'Authors with affiliations', 'Affiliations','Author Keywords', 'Authors', 'Authors with affiliations',
                        'Conference date','Conference name','Correspondence Address','Document Type','DOI','Funding Details',
                        'Funding Text 1','Funding Text 2','Funding Text 3','Index Keywords','ISBN','ISSN',
                        'Language of Original Document','Link','Publisher','Source title','Title','Year']

scopus_columns_list = [ 'code', 'author','university','faculty','school','group','city','department','country','address','others',
                        'Addresses','Affiliations', 'Article Title','Article Date' ,'Author Full Names', 'Author Keywords','Authors', 'Date of Export', 
                        'Document Type', 'DOI', 'DOI Link', 'eISSN', 'Email Addresses','Funding Name Preferred', 'Funding Orgs', 
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

for i in range(0,len(new_df)):
    source_string=new_df['Authors with affiliations'][i]
    dic_authors_with_affiliations=obj_scopus.authors_with_affiliations_process(source_string)
    consecutivo_articulo+=1
    if(len(dic_authors_with_affiliations)>0):
        new_record_scopus=[]
        for item in dic_authors_with_affiliations.items():
            consecutivo_autor=0
        
            list_columns_data = []
            consecutivo_autor+=1
            code='scopus-'+ year + '-' + str(consecutivo_articulo) + '-' + str(consecutivo_autor)

            print(code)
            url_doi="NE"
            fecha_articulo_string ="NE"
            if str(new_df['DOI'][i]).strip()=="" or pd.isna(new_df['DOI'][i]):
                fecha_articulo_string="NP"
            else:
                url_doi="https://doi.org/api/handles/" + new_df['DOI'][i] + "?type=HS_ADMIN"
                res = requests.get(url_doi)
                if(res.status_code==200):
                    json = res.json()
                    dic_values = json["values"][0]
                    fecha_articulo_string = dic_values["timestamp"]
                    fecha_articulo_string = fecha_articulo_string[0:10]
                
                list_columns_data.append(code)
                list_columns_data.append(item[1]['autor'])
                list_columns_data.append(item[1]['universidad'])
                list_columns_data.append(item[1]['facultad'])
                list_columns_data.append(item[1]['escuela'])
                list_columns_data.append(item[1]['grupo'])
                list_columns_data.append(item[1]['ciudad'])
                list_columns_data.append(item[1]['departamento'])
                list_columns_data.append(item[1]['pais'])
                list_columns_data.append(item[1]['direccion'])
                list_columns_data.append(item[1]['otros'])

                list_columns_data.append(new_df['Authors with affiliations'][i])
                list_columns_data.append(new_df['Affiliations'][i])
                list_columns_data.append(new_df['Title'][i])
                list_columns_data.append(fecha_articulo_string)
                list_columns_data.append('NE')
                list_columns_data.append(new_df['Author Keywords'][i])
                list_columns_data.append(new_df['Authors'][i])
                list_columns_data.append('NE')

                list_columns_data.append(new_df['Document Type'][i])
                list_columns_data.append(new_df['DOI'][i])
                list_columns_data.append(new_df['Link'][i])
                list_columns_data.append('NE')
                list_columns_data.append(new_df['Correspondence Address'][i])
                list_columns_data.append(new_df['Funding Details'][i])
                list_columns_data.append(new_df['Funding Text 1'][i])

                list_columns_data.append(new_df['Funding Text 2'][i])
                list_columns_data.append(new_df['ISBN'][i])
                list_columns_data.append(new_df['ISSN'][i])
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