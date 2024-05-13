#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 18:39:48 2024

@author: fremi
"""
import os
import sqlite3
# import pandas as pd

from .about import About
from .bakery import Bakery
from .logistic import Logistic
from .sales import Sales
from .cooperation import Cooperation
from .table import Table, Column

class Farm():
    def __init__(self, path):
        if not os.path.isfile(path):
            try:
                conn = sqlite3.connect(path)
                
            except sqlite3.OperationalError:
                print('Erreur la table existe déjà')
            except Exception as e:
                print("Erreur")
                conn.rollback()
                # raise e
            finally:
                self.conn = conn
                
                self._commit("PRAGMA foreign_keys = ON")
                
        else:
            try: conn = sqlite3.connect(path)
            except sqlite3.OperationalError:
                print('La base n''existe pas. Création.')
            
            self.conn = conn
        
        self.file_name = os.path.splitext(os.path.basename(path))[0]
        self.path = path
        
        self.about = About(conn=self.conn, farm=self)
        self.logistic = Logistic(conn=self.conn, farm=self)
        self.bakery = Bakery(conn=self.conn, farm=self)
        self.sales = Sales(conn=self.conn, farm=self)
        self.cooperation = Cooperation(conn=self.conn, farm=self)
        self.about.update_version()
        
        self.tmp_folders = []
        
    def _commit(self, query, var=None):
        print(query)
        
        cursor = self.conn.cursor()
        if var is None:
            cursor.execute(query)
        else:
            cursor.execute(query, var)
        self.conn.commit()    
        
    def close(self):
        self.conn.close()
        
    