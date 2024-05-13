# -*- coding: utf-8 -*-

from .table import Table, Column
version = 0.0

class About(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'about'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='paille_version',
                          sql_type='TEXT',
                          default='0.0')
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
        
        self.insert_entry(paille_version='0.0')
    
    def update_version(self):
        self.update_entry(i=0, paille_version=version)