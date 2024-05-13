# -*- coding: utf-8 -*-

from ..table import Table, Column

class Stock(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'logistic_stock'
        
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='logistic_goods_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('logistic_goods','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='date',
                          sql_type='INTEGER',
                          default=0),
                   Column(name='quantity',
                          sql_type='REAL',
                          default=0.0)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)