# -*- coding: utf-8 -*-

class PersonaMigrate(object):
 
    def __init__(self):
        pass

    def name_process(self,name_to_process,apellidos=None):
        words = name_to_process.split()
        num_words = len(words)
        apellidos_process = ''
        nombres_process = ''
        if num_words == 2:
            apellidos_process = words[0]
            nombres_process = words[1]
        elif num_words == 3:
            if apellidos != None:
                if (words[0] +' '+words[1])==apellidos:
                     apellidos_process = words[0] +' '+words[1]
                     nombres_process = words[2]
                else:
                     apellidos_process = words[0] 
                     nombres_process = words[1] +' '+words[2]
            else:
                apellidos_process = words[0] +' '+words[1]
                nombres_process = words[2]
        elif num_words == 4:
            apellidos_process = words[0] +' '+words[1]
            nombres_process = words[2]+' '+words[3]
        elif num_words >= 5:
            if apellidos != None:
                if (words[0] +' '+words[1])==apellidos:
                     apellidos_process = words[0] +' '+words[1]
                     for i in range(2,len(words)):
                        nombres_process = nombres_process + words[i]+' '
                elif (words[0] +' '+words[1]+' '+words[2])==apellidos:
                     apellidos_process = words[0] +' '+words[1] + ' '+ words[2]
                     for i in range(3,len(words)):
                        nombres_process = nombres_process + words[i]+' '
                else:
                     apellidos_process = words[0] +' '+words[1]
                     for i in range(2,len(words)):
                        nombres_process = nombres_process + words[i]+' '
            else:
                apellidos_process = words[0] +' '+words[1]
                for i in range(2,len(words)):
                    nombres_process = nombres_process + words[i]+' '
        nombres_process=nombres_process.rstrip()
        return apellidos_process, nombres_process

