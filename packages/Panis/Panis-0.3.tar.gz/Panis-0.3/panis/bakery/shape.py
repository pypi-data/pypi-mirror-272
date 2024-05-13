# -*- coding: utf-8 -*-

from ..table import Table, Column

class Shape(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_shape'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT'),
                   Column(name='code',
                          sql_type='TEXT'),
                   Column(name='position',
                          sql_type='REAL',
                          default=0.0)]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
