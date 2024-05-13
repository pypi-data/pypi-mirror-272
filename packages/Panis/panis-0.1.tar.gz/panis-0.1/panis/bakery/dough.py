# -*- coding: utf-8 -*-

from ..table import Table, Column

class Dough(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_dough'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT'),
                   Column(name='baking_weight_loss_inverse',
                          sql_type='REAL',
                          default=1.21),
                   Column(name='sourdough',
                          sql_type='BOOLEAN',
                          default=0),
                   Column(name='old_sourdough',
                          sql_type='BOOLEAN',
                          default=0),
                   Column(name='king_sourdough_weight',
                          sql_type='REAL',
                          default=1.0),
                   Column(name='extra_dough',
                          sql_type='REAL',
                          default=0.01),
                   Column(name='position',
                          sql_type='REAL',
                          default=0.0)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)