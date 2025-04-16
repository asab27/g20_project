# -*- coding: utf-8 -*-

import sys
import datetime
import sqlite3
class Gclass:
   
    def __init__(self):
        pass

    @classmethod
    def from_string(cls, str_data):
        str_list = str_data.split(";")
        return cls(*str_list)

    @classmethod
    def reset(cls):
        cls.obj = dict()
        cls.lst = list()
        cls.pos = 0
    
    @classmethod
    def get_id(cls, id):

        id = int(id)
        if id == 0:
            if len(cls.lst) == 0:
                id = 1
            else:
                id = max(cls.lst) + 1
        return id
   
    @classmethod
    def getlines(cls, att, value):
        return [obj.id for obj in list(cls.obj.values()) if getattr(obj, att) == value]
    
    @classmethod
    def nextrec(cls):
        cls.pos += 1
        return cls.current()
    @classmethod
    def previous(cls):
        cls.pos -= 1
        return cls.current()
    @classmethod
    def current(cls, code = None):
        if code in cls.lst:
            cls.pos = cls.lst.index(code)
        if cls.pos < 0:
            cls.pos = 0
            return None
        elif cls.pos >= len(cls.lst):
            cls.pos = len(cls.lst) - 1
            return None
        else:
            code = cls.lst[cls.pos]
            return cls.obj[code]
    @classmethod
    def first(cls):
        cls.pos = 0
        return cls.current()
    @classmethod
    def last(cls):
        cls.pos = len(cls.lst) - 1
        return cls.current()
 
    @classmethod
    def get_primary_keys(cls):
        return getattr(cls, "primary_keys", [cls.att[0]])

    @classmethod
    def get_obj_key(cls, obj):
        keys = cls.get_primary_keys()
        return "_".join(str(getattr(obj, k)) for k in keys)

    @classmethod
    def remove(cls, key):
        obj = cls.obj[key]
        where_clause = " AND ".join(
            f"{k}={cls.conv(obj, k, getattr(obj, k))}" for k in cls.get_primary_keys()
        )
        command = f'DELETE FROM {cls.__name__} WHERE {where_clause}'
        cls.sqlexe(command)
        cls.lst.remove(key)
        del cls.obj[key]
  
    @classmethod
    def insert(cls, key):
        obj = cls.obj[key]
        command = f'INSERT INTO {cls.__name__} VALUES('
        for att in cls.att:
            value = getattr(obj, att)
            command += f'{cls.conv(obj, att, value)},'
        command = command[:-1] + ")"
        cls.sqlexe(command)
  
    @classmethod
    def update(cls, key):
        obj = cls.obj[key]
        set_clause = ", ".join(
            f"{att[1:]} = {cls.conv(obj, att, getattr(obj, att))}" for att in cls.att[1:]
        )
        where_clause = " AND ".join(
            f"{k} = {cls.conv(obj, k, getattr(obj, k))}" for k in cls.get_primary_keys()
        )
        command = f'UPDATE "{cls.__name__}" SET {set_clause} WHERE {where_clause}'
        print(command)
        cls.sqlexe(command)
    @staticmethod
    def conv(obj, att, value):
        v = getattr(obj, att)
        if type(v) == str or type(v) == datetime.date:
            ret = f'"{value}"'
        else:
            ret = f'{value}'
        return ret
 
    @classmethod
    def orderfunc(cls, e):
        return getattr(cls.obj[e], cls.sortkey)
    @classmethod
    def sort(cls, att, reverse = False):
        cls.sortkey = att
        cls.lst.sort(key=cls.orderfunc, reverse= reverse)
    
    @classmethod
    def find(cls, value, att):
        lobj = cls.obj.values()
        fobj = [obj for obj in lobj if getattr(obj, att) == value]
        return fobj

    @classmethod
    def set_filter(cls, f_dic = {}):
        if f_dic:
            code = cls.att[0]
            lobj = cls.obj.values()
            s = set()
            for att,listf in f_dic.items():
                s1 = set([getattr(obj, code) for obj in lobj if getattr(obj, att) in listf])
                s = s.union(s1)
            if len(s) > 0:
                cls.lst = list(s)
                cls.pos = 0
        else:
            obj = cls.current()
            cls.lst = list(cls.obj.keys())
            code = cls.att[0]
            cls.current(getattr(obj, code))
    
    @classmethod
    def getatlist(cls, att):
        return [getattr(obj, att) for obj in list(cls.obj.values())]

    @classmethod
    def read(cls, path = ''):
        cls.obj = dict()
        cls.lst = list()
        cls.path = path
        try:
            fh = open(path, 'r')
            fh.close()
            lista = cls.sqlexe("select * from " + cls.__name__)
            if lista != None:
                for r in lista:
                    objstr = f'{r[0]}'
                    for att in range(1,len(lista[0])):
                        objstr += f';{r[att]}'
                    cls.from_string(objstr)
        except FileNotFoundError:
            print(f"ERROR: {path} data file not found")
        except BaseException as err:
            print(f"Error in read method:\n{err}\n{type(err)}")
            sys.exit()
   
    def __str__(self):
        strprint = "f'"
        for att in type(self).att:
            strprint += '{self.' + att + '};'
        strprint = strprint[:-1] + "'"
        return eval(strprint)
 
    @classmethod
    def sqlexe(cls, command):
        resul = None
        try:
            con = sqlite3.connect(cls.path)
            cur = con.cursor()
            con.row_factory = sqlite3.Row
            tname = cls.__name__
            cur = con.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tname}'")
            table = cur.fetchone()
            if table is None or table[0] != tname:
                print(f"ERROR: table {tname} missing in database {cls.path}")
                sys.exit()
            cur = con.execute(command)
            resul = cur.fetchall()
            con.commit()
            con.close()
        except sqlite3.Error as er:
            print(f'sqlite error: {er}')
        return resul
