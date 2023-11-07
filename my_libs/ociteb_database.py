# -*- coding: utf-8 -*-
 
import pymysql
 
class DatabaseUtil(object):
 
    def __init__(self):
        # Variable que determina si estamos conectados a MySQL...
        self.connected=0
        self.error=""
 
    def mysql_connect(self,host,user,pw,database,port=3306):
        """
        Realiza la conexion con la base de datos
        Tiene que recibir:
            - host
            - user
            - pw => password
            - database => database name
        Puede recibir:
            - port
        Devuelve True o False
        """
        try:
            self.db = pymysql.connect(user=user, 
                                        passwd=pw, 
                                        host=host, 
                                        db=database, 
                                        port=port, 
                                        charset="utf8", 
                                        init_command="set names utf8")
            self.cursor = self.db.cursor()
            self.connected=1
            return True
        except Exception as e:
            self.error="Error: %s" % (e)
        except:
            self.error="Error desconocido"
        return False
 
    def prepare_query(self,query,params=None):
        if self.connected:
            self.error=""
            try:
                self.cursor.execute(query,params)
                result = []
                columns = tuple([d[0] for d in self.cursor.description])
                for row in self.cursor:
                    result.append(dict(zip(columns, row)))
                return result
            except Exception as e:
                self.error="Error: %s" % (e)
        return False
 
    def prepare_operation(self,query,params=None):
        if self.connected:
            self.error=""
            try:
                self.cursor.execute(query,params)
                self.db.commit()
                return True
            except Exception as e:
                self.error="Error: %s" % (e)
                return self.error
        return False
 
    def last_id(self):
        """
        Funcion que devuelve el ultimo id añadido
        """
        return self.cursor.lastrowid
 
    def affected_rows(self):
        return self.cursor.rowcount
 
    def mysql_close(self):
        """
        Funcion para cerrar la conexion con la base de datos
        """
        self.connected=0
        try:
            self.cursor.close()
        except:pass
 
    def fetch_one_assoc(self,cursor) :
        data = cursor.fetchone()
        if data == None :
            return None
        desc = cursor.description
 
        dict = {}
 
        for (name, value) in zip(desc, data) :
            dict[name[0]] = value
 
        return dict
 