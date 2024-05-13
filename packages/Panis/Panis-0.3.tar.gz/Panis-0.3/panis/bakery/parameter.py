# -*- coding: utf-8 -*-

from ..table import Table, Column

class Parameter(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_parameter'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='extra_dough',
                          sql_type='REAL',
                          default=0.01)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
        
        if self.get_entry(i=1) is None:
            self.insert_entry()