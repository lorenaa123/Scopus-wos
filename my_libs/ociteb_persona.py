# -*- coding: utf-8 -*-
 
class Persona(object):
 
    def __init__(self):
        self.dict_persona = {
            'id'              : 0 ,
            'identificacion'  : '',
            'apellidos'       : '',
            'nombres'         : '',
            'genero'          : 'F',
            'fecha_nacimiento': ''
        }

    def set_identificacion(self,identificacion):
        self.dict_persona['identificacion'] = identificacion

    def set_apellidos(self,apellidos):
        self.dict_persona['apellidos'] = apellidos

    def set_nombres(self,nombres):
        self.dict_persona['nombres'] = nombres
    
    def set_genero(self,genero):
        self.dict_persona['genero'] = genero

    def set_fecha_nacimiento(self,fecha_nacimiento):
        self.dict_persona['fecha_nacimiento'] = fecha_nacimiento

    def get_identificacion(self,):
        return self.dict_persona['identificacion'] 

    def get_apellidos(self,):
        return self.dict_persona['apellidos'] 

    def get_nombres(self,):
        return self.dict_persona['nombres'] 
    
    def get_genero(self,):
        return self.dict_persona['genero'] 

    def get_fecha_nacimiento(self,):
        return self.dict_persona['fecha_nacimiento'] 
