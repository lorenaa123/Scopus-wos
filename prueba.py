import my_libs.ociteb_utils  as ou
cadena = "Manrique-Abril, F.G., FM: RN. AB. Ph. D. Salud Pública; Ph.D. Investigación Clínica. Investigador, Instituto de Salud Pública. Profesor Titular, Facultad de Enfermería. Universidad Nacional de Colombia. Bogotá, Colombia. Universidad Pedagógica y tecnológica de Colombia. fgmanriquea@unal.edu.co; Agudelo-Calderon, C.A., CA. MD. Periodista. M. Sc. Salud Pública.M. Sc. Ciencias. Instituto de Salud Pública. Facultad de Medicina. Universidad Nacional de Colombia. Bogotá, Colombia; González-Chordá, V.M., VG: RN. M. Sc. Enfermería. Ph.D. Ciencias de la Salud. Profesor ayudante doctor. Departamento de Enfermería. Universitat Jaume I. España.; Gutiérrez-Lesmes, O., OG. RN. Esp. Epidemiologia. M. Sc. Gestión Ambiental Sostenible. Ph. D(c). Epidemiologia. Profesor Asociado, Escuela de Salud Pública. Universidad de los Llanos. Villavicencio, Colombia; Téllez-Piñerez, C.F., CT. Estadístico. M. Sc. Ciencias Estadística. Ph.D(c). Ciencias. Estadística. Profesor, Universidad Santo Tomas. Bogotá, Colombia; Herrera-Amaya, G., GH. RN. M. Sc. Investigación en APD. Ph.D(c). Ciencias Enfermería. Profesora Asistente. Universidad Pedagógica y Tecnológica de Colombia. Grupo de Salud pública, Colombia"

def authors_with_affiliations_process(source_string):
    if isinstance(source_string, str):
        source_list = source_string.split(";")
        dic_addresses_records = {}
        key_ord = 1
        for record in source_list:
            new_record = ou.String_utils.replace_accents(record)
            position = ou.String_utils.search_index_char(new_record, '., ')
            author = new_record[0:position]
            # Verifica si el autor tiene menos de 100 caracteres
            if len(author) < 100:
                filation_data = new_record[position + 2:]
                key = str(key_ord)
                dic_addresses_records[key] = author
                key_ord += 1
        return dic_addresses_records
    else:
        print("error")

result = authors_with_affiliations_process(cadena)
print(result)
