import pandas as pd
import  my_libs.ociteb_dataframe  as od

dic_Facultad_ciudad={
    'CIENCIAS':'TUNJA',
    'CIENCIAS AGROPECUARIAS':'TUNJA',
    'CIENCIAS DE LA EDUCACION':'TUNJA',
    'CIENCIAS DE LA SALUD':'TUNJA',
    'CIENCIAS ECONOMICAS Y ADMINISTRATIVAS':'TUNJA',
    'DERECHO Y CIENCIAS SOCIALES':'TUNJA',
    'ESTUDIOS A DISTANCIA':'TUNJA',
    'INGENIERIA':'TUNJA',
    'SECCIONAL CHIQUINQUIRA':'CHIQUINQUIRA',
    'SECCIONAL DUITAMA':'DUITAMA',
    'SECCIONAL SOGAMOSO':'SOGAMOSO',
    'DESCONOCIDA':'DESCONOCIDA'
}

array_uptc_names = [
    ', Universidad Pedagógica y Tecnológica de Colombia and Universidad de Boyacá',
    ' Universidad Pedagógica y Tecnológica de Colombia and Universidad de Boyacá',
    'Universidad Pedagógica y Tecnológica de Colombia and Universidad de Boyacá',
    'UNIVERSIDAD PEDAGOGICA Y TECNOLOGICA DE COLOMBIA',
    'PEDAGOGICAL AND TECHNOLOGICAL UNIVERSITY OF COLOMBIA',
    'UNIV PEDAG & TECNOL COLOMBIA',
    'Univ Pedag & Tecnol Colombia UPTC',
    'PEDAG & TECHNOL UNIV COLOMBIA',
    'UNIVERSIDAD PEDAGOGICA Y TECNOLOGICA DE COLOMBIA',
    'PEDAGOGICAL AND TECHNOLOGICAL UNIVERSITY OF COLOMBIA',
    'UNIV PEDAG & TECNOL COLOMBIA',
    'Univ Pedag & Tecnol Colombia UPTC',
    'PEDAG & TECHNOL UNIV COLOMBIA',
    ' Universidad Pedagógica y Tecnológica de Colombia ',
    'Universidad Pedagógica y Tecnológica de Colombia ',
    ' Universidad Pedagógica y Tecnológica de Colombia',
    ' Universidad Pedagógica y Tecnológica de Colombia UPTC ',
    'PEDAGOGICAL AND TECHNOLOGICAL UNIVERSITY OF COLOMBIA ',
    'UNIV PEDAG & TECNOL COLOMBIA ',
    ' Univ Pedag & Tecnol Colombia UPTC ',
    ' PEDAG & TECHNOL UNIV COLOMBIA ',
    ' UPTC',
    ' U.P.T.C.',
    ' Universidad Pedagógica y Tecnológica',
    ' Universidad Pedagógica y Tecnológica - Colombia',
    ' Pedagogical and Technological University of Colombia',
    ' Universidad Pedagógica y Tecnológica (UPTC)',
    ' Univ. Pedagógica y Tecnológica de Colombia',
    ' UPTC - Universidad Pedagógica y Tecnológica de Colombia',
    ' Universidad Pedagógica y Tecnológica de Colombia (UPTC)',
    ' Pedagogical and Technological Univ. of Colombia',
    ' UPTC - Univ. Pedagógica y Tecnológica de Colombia',
    ' Pedagógica y Tecnológica Univ. of Colombia',
    ' UPTC - Pedagógica y Tecnológica Univ. of Colombia',
    ' Pedagógica y Tecnológica de Colombia University',
    ' UPTC - Pedagógica y Tecnológica de Colombia University',
    ' Univ. Pedagógica y Tecnológica - UPTC',
    ' Universidad Pedagógica y Tecnológica de Colombia (U.P.T.C.)',
    ' UPTC - Universidad Pedagógica y Tecnológica',
    ' Universidad Pedagógica y Tecnológica de Colombia (Pedagógica)',
    ' Universidad Pedagógica y Tecnológica de Colombia (Tecnológica)',
    ' Universidad Pedagógica y Tecnológica de Colombia (Colombia)',
    ' Universidad Pedagógica y Tecnológica de Colombia - UPTC',
    ' UPTC - Universidad Pedagógica y Tecnológica de Colombia (UPTC)',
    ' Universidad Pedagógica y Tecnológica de Colombia (UPTEC)',
    ' UPTC - Universidad Pedagógica y Tecnológica de Colombia (UPTEC)',
    ' Pedagogical and Technological Univ. of Colombia (UPTC)',
    ' UPTC - Pedagogical and Technological Univ. of Colombia',
    ' Pedagógica y Tecnológica Univ. of Colombia (UPTC)',
    ' UPTC - Pedagógica y Tecnológica Univ. of Colombia',
    ' Pedagógica y Tecnológica de Colombia University (UPTC)',
    ' UPTC - Pedagógica y Tecnológica de Colombia University',
    ' Univ. Pedagógica y Tecnológica - UPTC (Colombia)',
    ' UPTC - Universidad Pedagógica y Tecnológica (Colombia)',
    ' Universidad Pedagógica y Tecnológica de Colombia (UPTC - Colombia)',
    ' UPTC - Universidad Pedagógica y Tecnológica de Colombia (UPTC - Colombia)',
    ' Universidad Pedagógica y Tecnológica de Colombia (UPTEC - Colombia)',
    ' UPTC - Universidad Pedagógica y Tecnológica de Colombia (UPTEC - Colombia)',
    ' Pedagogical and Technological Univ. of Colombia (UPTC - Colombia)',
    ' UPTC - Pedagogical and Technological Univ. of Colombia (UPTC - Colombia)',
    ' Pedagógica y Tecnológica Univ. of Colombia (UPTC - Colombia)',
    ' UPTC - Pedagógica y Tecnológica Univ. of Colombia (UPTC - Colombia)',
    ' Pedagógica y Tecnológica de Colombia University (UPTC - Colombia)',
    ' UPTC - Pedagógica y Tecnológica de Colombia University (UPTC - Colombia)',
     'Universidad Pedagógica Tecnológica de Colombia',
 'Universidad Pedagógica y Tecnológica de',
 'Universidad Pedagógica y Tecnológica d Tunja',
 'Universidad Pedagógica y Tecnológica de Colombia - Sede Tunja'

]

array_synonyms_universidad = [
    'UNIV',
    'UNIVERSIDAD',
    'UNIVERSITY'
]

array_synonyms_facultad = [
    'FACULTAD',
    'FAC',
    'FACULTY'
]

array_synonyms_escuela = [
    'ESCUELA',
    'DEP',
    'DEPT',
    'DEPARTAMENTO',
    'PROGRAM',
    'PROGRAMA',
    'SCH',
    'TRANSPORTE & VIAS'
]

array_synonyms_grupo = [
    'GRUPO',
    'GRP',
    'GEBIMOL',
    'GEO',
    'GEOC',
    'GIMI'
]

array_synonyms_departamento = [
    'AMAZONAS',
    'ANTIOQUIA',
    'ARAUCA',
    'ATLANTICO',
    'BOLIVAR',
    'BOYACA',
    'BOY',
    'CALDAS',
    'CAQUETA',
    'CASANARE',
    'CAUCA',
    'CESAR',
    'CHOCO',
    'CORDOBA',
    'CUNDINAMARCA',
    'DISTRITO CAPITAL',
    'GUAINIA',
    'GUAJIRA',
    'GUAVIARE',
    'HUILA',
    'MAGDALENA',
    'META',
    'NARIÑO',
    'NORTE DE SANTANDER',
    'PUTUMAYO',
    'QUINDIO',
    'RISARALDA',
    'SAN ANDRES Y PROVIDENCIA',
    'SANTANDER',
    'SUCRE',
    'TOLIMA',
    'VALLE DEL CAUCA',
    'VAUPES',
    'VICHADA',
]

array_synonyms_ciudad = [
    'CALI',
    'CIUDAD',
    'CHIQUINQUIRA',
    'BOGOTA',
    'DUITAMA',  
    'SOGAMOSO',
    'TUNJA',
    'VILLAVICENCIO'
]

array_synonyms_direccion = [
    'AVE',
    'AV',
    'AVENIDA',
    'CALLE',
    'CAMPUS',
    'CARRERA',
    'CRA',
    'CR',
    'DIAGONAL'  
]

array_synonyms_research_site = [
    'CLIN',
    'CTR', 
    'DOCTORADO',
    'GARDEN',
    'GARDENS',
    'HERBARIO',
    'IN',
    'INST',
    'INSTITUTO',
    'JARDIN',
    'LAB',
    'LABORATORY',
    'LABORATORIO',
    'MUSE',
    'MUSEO',
    'MUSEUM',  
    'SEDE',
    'SECRETARIA',
    'UNIDAD'
]

def get_countries():
    SOURCE_PATH = './data/origin/'
    SOURCE_FILE_MAIN = 'paises.xlsx'

    sheet_main  = od.Sheet_dataframe(SOURCE_PATH + SOURCE_FILE_MAIN)
    series_select_list = ['NOMBRE', 'NAME']
    sheet_main.generate_new_dataframe(series_select_list)
    new_df=sheet_main.get_new_dataframe()
    array_synonyms_pais_nombre  = new_df['NOMBRE']
    array_synonyms_pais_name  =  new_df['NAME']
    array_synonyms_pais = pd.concat([array_synonyms_pais_name,array_synonyms_pais_nombre])

    return array_synonyms_pais

array_synonyms_pais  =  get_countries()

