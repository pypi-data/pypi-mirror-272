# -*- coding: utf-8 -*-

from ..table import Table, Column

class Delivery(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'sales_delivery'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT',
                          default=''),
                   Column(name='position',
                          sql_type='REAL',
                          default=0.0),
                   Column(name='address',
                          sql_type='TEXT',
                          default=''),
                   Column(name='postal_code',
                          sql_type='INTEGER',
                          default=0),
                   Column(name='city',
                          sql_type='TEXT',
                          default=''),
                   Column(name='note',
                          sql_type='TEXT',
                          default=''),
                   Column(name='new_page',
                          sql_type='BOOLEAN',
                          default=0),
                   Column(name='unsold_line',
                          sql_type='BOOLEAN',
                          default=0),
                   Column(name='market_sheet',
                          sql_type='BOOLEAN',
                          default=0)]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
