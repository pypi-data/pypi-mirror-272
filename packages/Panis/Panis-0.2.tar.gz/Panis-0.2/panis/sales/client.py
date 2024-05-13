# -*- coding: utf-8 -*-

from ..table import Table, Column

class Client(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'sales_client'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT',
                          default=''),
                   Column(name='first_name',
                          sql_type='TEXT',
                          default=''),
                   Column(name='phone',
                          sql_type='TEXT',
                          default=''),
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
                          default='')]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)